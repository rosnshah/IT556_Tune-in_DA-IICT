from random import randint
import math
from scipy import spatial
import numpy
from sklearn.metrics.pairwise import cosine_similarity


max_songs = 24896  #Number of songs in database
rec_songs=10       #Number of songs to suggest in 1 recommendation
rec_genre= 3       #Number of genres to look for in collaborative filtering
max_users=40       #Number of users
max_genre=60       #Number of maximum genres in database
beta = 0.6         #proportion by which songs will be suggested using col filtering from exploration quota
current_songs_id = [0]*rec_songs
current_songs_rating = [0]*rec_songs
users_status = [0]*(max_users+1)
user_backup = [[0]*(6) for _ in range(max_users+1)]
totalrating_count = [[0]*(max_genre+1) for _ in range(max_users+1)]
totalrating_sum = [[0]*(max_genre+1) for _ in range(max_users+1)]
user_song_rating = [[0]*(max_songs+1) for _ in range(max_users+1)]
predicted_ratings = [0]*(max_songs+1)
similarity_score = [0]*(max_songs+1)
song_mapping = [0]*(max_songs+1)
genre_mapping=[0]*(max_genre+1)
vector_a=[0]*(max_users+1)
vector_b=[0]*(max_users+1)

#Gives the genre_id of the given song
def get_genre(song_id):
    fp = open("songs.txt", 'r')
    genre_id = 0;
    line = fp.readline()
    line = fp.readline()
    while line:
        temp = line.split(',')
        if int(temp[0]) == song_id:
            genre_id = temp[2]
            break;
        line = fp.readline()

    return genre_id


#Generate genre-song matrix
def generateArray():
    fp = open("songs.txt", 'r')
    line = fp.readline()
    line = fp.readline()
    genre_songs = [[0]*1000 for _ in range(max_genre+1)];
    genre_count = [0]*(max_genre+1)
    #j=0;
    while line:
        #print(j)
        #j=j+1
        tmp = line.split(',')

        genre_no=int(tmp[2])
        count=int(genre_count[genre_no])

        genre_count[genre_no]=genre_count[genre_no]+1;
        genre_songs[genre_no][count]=int(tmp[0]);
        line = fp.readline()
    return genre_songs

#update the all the ratings matrix
def updateRatings():

    for index in range(len(current_songs_id)):
        song_id = int(current_songs_id[index])
        user_song_rating[userID][song_id] = current_songs_rating[index]

    for index in range(len(current_songs_rating)):
        genre = int(get_genre(current_songs_id[index]))
        totalrating_sum[userID][genre] = totalrating_sum[userID][genre] + int(current_songs_rating[index])
        totalrating_count[userID][genre] = totalrating_count[userID][genre] + 1


#Recommend songs based on RL
def recommendSongs_rl(rl_songs,start_index):

    count = 0
    genre_selected = [0] * rec_genre
    flag = [0] * (max_genre+1)

    while count < rec_genre:
        max = -1;
        ind = -1;
        for i in range(1,max_genre):
            if (int(totalrating_count[userID][i]) == 0):
                continue;
            avg_rating = totalrating_sum[userID][i] / totalrating_count[userID][i]
            # print(avg_rating)
            if avg_rating > max and flag[i] is 0:
                max = avg_rating;
                ind = i

        genre_selected[count] = ind
        flag[ind] = 1
        count = count + 1

   # print(genre_selected)

    songs_selected = []
    genre_songs = generateArray()

    for i in range(rec_genre):
        genre = genre_selected[i]
        if (int(genre) == -1):
            continue;
        songs = genre_songs[genre]
        for song in songs:
            if int(user_song_rating[userID][song])!=0 or int(song) == 0:
                continue

            songs_selected.append(song)

    count = start_index
    #print(len(songs_selected))
    while count < start_index+rl_songs:
        r = randint(0,len(songs_selected))
        song = songs_selected[r]
        if current_songs_id.__contains__(song):
            continue
        current_songs_id[count] = song
        count = count + 1


#Recommend songs using collaborative Filtering
#Will only kick in after 30 iterations
def recommendSongs_col(col_songs):
    if col_songs == 0:
        return
    rating_matrix=[[0] * (max_users + 1) for _ in range(max_songs + 1)]
    temp = numpy.transpose(user_song_rating)
    # generate song-user matrix
    for i in range(len(temp)):
        for j in range(len(temp[i])):
            rating_matrix[i][j]=temp[i][j]

    #Subtract mean , so that pearson correlation can be counted
    for i in range(len(rating_matrix)):
        sum = 0
        count = 0
        mean = 0
        for j in range(len(rating_matrix[i])):
            if (int(rating_matrix[i][j]) != 0):
                sum = sum + int(rating_matrix[i][j])
                count = count + 1

        if (count != 0):
            mean = sum / count

        mag_square = 0
        for j in range(len(rating_matrix[i])):
            if (int(rating_matrix[i][j]) != 0):
                rating_matrix[i][j] = int(rating_matrix[i][j]) - mean

    for i in range(len(rating_matrix)):
        if (int(rating_matrix[i][userID]) != 0):
            predicted_ratings[i] = -1  # Already given by user
        else:
            vetor_a = rating_matrix[i]
            for j in range(len(rating_matrix)):
                vetor_b = rating_matrix[j]

                similarity_score[j] = cosine_similarity(vector_a,vector_b)
            # Assuming user has rated other 5 movies
            # finds top 5 indexes in vector most_similar for which user has rated
            knearest = 5
            most_similar = [0] * knearest
            flag = [0] * len(rating_matrix)
            count = 0
            while count < knearest:
                max_similarity = -1
                ind = -1
                for t in range(len(similarity_score)):
                    if similarity_score[t] == 1:
                        continue
                    temp = similarity_score[t]
                    if temp > max_similarity and flag[t] is 0:
                        max_similarity = temp
                        ind = t
                most_similar[count] = ind
                count = count + 1
                flag[ind] = 1

            prsum = 0
            prsimsum = 0
            for k in range(len(most_similar)):
                prsum = prsum + (int(rating_matrix[k][userID])) * similarity_score[k]
                prsimsum = prsimsum + similarity_score[k]

            predicted_ratings[i] = prsum / prsimsum

    # finds maximum 3 ratings from predicted_ratings.And get their song id to result
    count = 0
    flag = [0] * len(rating_matrix)
    while (count < col_songs):
        max_predicted = -1
        ind = -1
        for t in predicted_ratings:
            tmp = predicted_ratings[t]
            if tmp > max_predicted and tmp != -1 and flag[t] is 0:
                max_predicted = tmp
                ind = t
        current_songs_id[count] = ind
        count = count + 1
        flag[ind] = 1



#Recommend songs randomly for exploration
def recommendSongs_explore(exploration_songs,start_index):

    count = start_index
    while count < exploration_songs+start_index:
        r = randint(1,max_songs)
        if current_songs_id.__contains__(r):
            continue
        current_songs_id[count]=r
        count = count+1


#Backup the current data in the files
def backup():
    fp = open("user_songID.txt", 'w')
    fp.write("userID,songID,Rating\n")
    for i in range(1,41):
        if i==0:
            continue
        for j in range(1,max_songs+1):
            if j==0:
                continue
            fp.write(str(i)+","+str(j)+","+str(user_song_rating[i][j])+"\n")

    fp = open("user_backup.txt", 'w')
    fp.write("userID,iterations,alpha,flag,upper_limit,user_status\n")

    for i in range(1,41):
        if i!=0:
            fp.write(str(i)+","+str(user_backup[i][0])+","+str(user_backup[i][1])+","+str(user_backup[i][2])+","+str(user_backup[i][3])+","+str(users_status[i])+"\n")


#Read data saved earlier from the files
fp = open("songs.txt", 'r')
line = fp.readline()
line=fp.readline()
while line:
    arr = line.split(',')
    song_id = int(arr[0])
    song = arr[1]
    genre_id = int(arr[2])
    genre = arr[3]

    song_mapping[song_id]=song
    genre_mapping[genre_id] = genre

    line = fp.readline()

fp = open("user_songID.txt", 'r')
line = fp.readline()
line = fp.readline()

while line:
    arr = line.split(",")
    user_id= int(arr[0])
    songid = int(arr[1])
    song_rating = int(arr[2])
    user_song_rating[user_id][songid] = song_rating

    if song_rating > 0:
        genreid = int(get_genre(songid))

      #  print(genreid)
        totalrating_sum[user_id][genreid] = totalrating_sum[user_id][genreid] + song_rating
        totalrating_count[user_id][genreid] = totalrating_count[user_id][genreid] +1

    line = fp.readline()


fp = open("user_backup.txt", 'r')
line = fp.readline()
line = fp.readline()

while line:
   arr = line.split(",")
   id = int(arr[0])
   user_backup[id][0] = arr[1]
   user_backup[id][1] = arr[2]
   user_backup[id][2] = arr[3]
   user_backup[id][3] = arr[4]
   users_status[id] = arr[5]

   line = fp.readline()




while True:

    #Login for user
    print('Enter your userID')
    userID = int(input())

    # If this is new user, initially random songs will be suggested
    if int(users_status[userID]) == 0:
        users_status[userID]=1
        #Give 10 random songs initially
        count=0
        flag = [0]*max_songs
        while count<rec_songs:
            rand_song_id=randint(1,max_songs)
            if(int(flag[rand_song_id])==1):
                continue
            current_songs_id[count]=rand_song_id
            flag[rand_song_id]=1
            count=count+1
        print('Recommended songs are : ')

        for id in current_songs_id:
            print("Song : "+song_mapping[int(id)] + "   Genre : " + genre_mapping[int(get_genre(id))])
        print()

        print('Please rate each of the recommended songs. Thanks')
        count = 0
        while count < rec_songs:
            rating = input()
            current_songs_rating[count] = rating
            count = count + 1

        # Update ratings
        updateRatings()


    iteration = int(user_backup[userID][0])
    alpha = float(user_backup[userID][1])
    flag = int(user_backup[userID][2])
    lower_limit = 0.1
    upper_limit= float(user_backup[userID][3])
    change = 0.05
    checker = -1

    while True:
        # Recommend songs for the users based on exploration and exploitation ratio.
        print('Press 1 for new recommendation and 2 to log out and 3 to quit the program')
        checker = input()
        if int(checker) == 2:
            print('You have been logged out')
            break;
        elif int(checker) == 3:
            break

        exploration_songs=math.floor((rec_songs*(alpha)))
        exploitation_songs=math.ceil(rec_songs*(1-alpha))
        print(iteration)
        if iteration > 30:
            col_songs = math.floor(exploitation_songs*beta)
            rl_songs = math.ceil(exploitation_songs * (1 - beta))
        else:
            col_songs=0
            rl_songs = exploitation_songs

        recommendSongs_col(col_songs)
        recommendSongs_rl(rl_songs,col_songs)
        recommendSongs_explore(exploration_songs,col_songs+rl_songs)

        for id in current_songs_id:
            print("Song : " + song_mapping[int(id)] + "   Genre : " + genre_mapping[int(get_genre(id))])
        print()

        print('Please rate each of the recommended songs. Thanks')
        count = 0
        while count < rec_songs:
            rating = input()
            current_songs_rating[count] = rating
            count = count + 1

        # Update ratings
        updateRatings()


        if iteration%5 == 0:
            if flag==1:
                if alpha == upper_limit:
                    flag = flag*-1
                    alpha = alpha - change
                    if upper_limit> 0.1:
                        upper_limit = upper_limit - 0.1
                else:
                    alpha = alpha+change
            else:
                if alpha == lower_limit:
                    flag = flag*-1
                    alpha = alpha + change
                else:
                    alpha = alpha-change

        iteration=iteration+1

    user_backup[userID][0] = iteration
    user_backup[userID][1] = alpha
    user_backup[userID][2] = flag
    user_backup[userID][3] = upper_limit


    #If user  want to exit, save the current data and then exit.
    if int(checker) == 3:
        backup()
        print('Bye Bye')
        break

