from os import stat
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
import requests

from .handleDB import *
from .serializers import *

###############################################################################


@api_view(['POST'])
def register(request):
    """
    {
        "name": "Demo User 1",
        "user_name": "demouser1",
        "email": "demouser1@gmail.com",
        "password": "pswd_1"
    }
    """
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():

        data = serializer.data

        user_data = {
            'name': data['name'],
            'user_name': data['user_name'],
            'email': data['email'],
            'password': data['password'],
            'contributor': 0
        }

        email = data['email']
        user_name = data['user_name']

        if(check_valid_email(email)==0):
            return Response("INVALID EMAIL", status=status.HTTP_406_NOT_ACCEPTABLE)
        
        elif (check_email_exist(email) != 0):
            print("EMAIL ALREADY EXIST")
            return Response("EMAIL ALREADY EXIST", status=status.HTTP_406_NOT_ACCEPTABLE)

        elif(check_username_exist(user_name) != 0):
            print("EMAIL USER NAME EXIST")
            return Response("USER NAME ALREADY EXIST", status=status.HTTP_406_NOT_ACCEPTABLE)

        elif((check_email_exist(email) == 0) and (check_username_exist(user_name) == 0)):
            print("NEW USER FOUND")
            create_user(email, user_data)
            return Response("REGISTERED SUCCESSFULLY", status=status.HTTP_201_CREATED)
        else:
            print("ERROR IN REGISTERING, TRY AGAIN")
            return Response("ERROR IN REGISTERING, TRY AGAIN", status=status.HTTP_403_FORBIDDEN)

    else:
        return Response("INVALID SERIALIZED DATA", status=status.HTTP_400_BAD_REQUEST)

###############################################################################


@api_view(['POST'])
def login(request):
    
    """
    {
        "email": "demouser1@gmail.com",
        "password": "pass"
    }
    """
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():
        data = serializer.data
        
        email = data['email']
        password = data['password']

        # print(email)
        # print(password)

        if(check_email_exist(email) == 1):

            if(verify_login_by_email(email, password) == 1):
                print("LOGGED IN SUCCESFULLY")
                return Response("LOGGED IN SUCCESSFULLY", status=status.HTTP_200_OK)
            else:
                print("INVALID PASSWORD")
                return Response("Invalid Password !! Please Try Again", status=status.HTTP_401_UNAUTHORIZED)

        elif(check_email_exist(email) == -1):
            print("Cant verify email (-1)")
            return Response("PLEASE TRY AGAIN", status=status.HTTP_403_FORBIDDEN)

        else:
            print("EMAIL DOES NOT EXIST")
            return Response("PLEASE REGISTER", status=status.HTTP_404_NOT_FOUND)

    else:
        return Response("INVALID SERIALIZED DATA", status=status.HTTP_400_BAD_REQUEST)


###############################################################################


@api_view(['POST'])
def register_contributor(request):
    """
    {
        "email": "demouser1@gmail.com",
        "college": "RCOEM",
        "semester": "2nd",
        "branch" : "CSE A",
        "linkedin_url" : "https://www.demouser1.com",
        "github_url" : "https://www.github.demouser1.com",
        "codechef_url" : "https://www.codechef.demouser1.com",
        "codeforces_url" : "https://www.codeforces.demouser1.com",
        "leetcode_url" : "https://www.leetcode.demouser1.com",
        "other_url" : "https://www.demouser1.com",
        "company" : "",
        "position" : "",
        "skills": "C++,C,JAVA,demouser1"
    }
    """
    serializer = AuthenticateSerializer(data=request.data)

    if serializer.is_valid():
        data = serializer.data

        email = data['email']
        college = data['college']
        semester = data['semester']
        branch = data['branch']
        skills_str = data['skills']
        linkedin_url = data['linkedin_url']
        github_url = data['github_url']
        codechef_url = data['codechef_url']
        codeforces_url = data['codeforces_url']
        leetcode_url = data['leetcode_url']
        other_url = data['other_url']
        company = data['company']
        position = data['position']

        points = 0
        skills = covert_string_to_skills_list(skills_str)

        user_data = {
            'college': college,
            'semester': semester,
            'branch': branch,
            'skills': skills,
            'points': points,
            'contributor': 1,
            'linkedin_url': linkedin_url,
            'github_url': github_url,
            'codechef_url': codechef_url,
            'codeforces_url': codeforces_url,
            'leetcode_url': leetcode_url,
            'other_url': other_url,
            'company': company,
            'position': position
        }

        if (check_email_exist(email) == 0):
            print("NO USER FOUND")
            return Response("NO USER FOUND", status=status.HTTP_404_NOT_FOUND)

        elif (check_email_exist(email) == -1):
            print("ERROR")
            return Response("PLEASE TRY AGAIN", status=status.HTTP_403_FORBIDDEN)

        elif (check_email_exist(email) == 1):

            print("USER FOUND")

            if(add_authentication_user_data(email, user_data) == 1):
                return Response("PROFILE UPDATED", status=status.HTTP_200_OK)
            else:
                print("ERROR IN UPDATING DATA")
                return Response("PLEASE TRY AGAIN", status=status.HTTP_403_FORBIDDEN)

    return Response("INVALID DATA", status=status.HTTP_400_BAD_REQUEST)

###############################################################################
    
@api_view(['POST'])
def update_password(request):
    """
    {
        "email": "demouser4@gmail.com",
        "password": "updated_password"
    }
    """
    serializer = UpdatePasswordSerializer(data=request.data)

    if serializer.is_valid():
        data = serializer.data
        
        email = data['email']
        password = data['password']

        # print(email)
        # print(password)

        if(check_email_exist(email) == 1):

            if(updatePassword(email, password) == 1):
                print("Password Updated Successfully")
                return Response("Password Updated Successfully", status=status.HTTP_200_OK)
            else:
                print("Cant update Password")
                return Response("FAILED TO UPDATE PASSWORD, PLEASE TRY AGAIN", status=status.HTTP_403_FORBIDDEN)

        elif(check_email_exist(email) == -1):
            print("Cant verify email (-1)")
            return Response("PLEASE TRY AGAIN", status=status.HTTP_403_FORBIDDEN)

        else:
            print("EMAIL DOES NOT EXIST")
            return Response("EMAIL DOES NOT EXIST", status=status.HTTP_404_NOT_FOUND)

    else:
        return Response("INVALID SERIALIZED DATA", status=status.HTTP_400_BAD_REQUEST)


###############################################################################


@api_view(['GET'])
def view_all_questions(request):

    data = get_all_questions()
    return Response(data)

###############################################################################

@api_view(['GET'])
def view_search_questions(request):

    data = get_search_questions()
    return Response(data)

###############################################################################


@api_view(['GET'])
def view_trending_questions(request):

    data = get_trending_questions()
    return Response(data)

###############################################################################


@api_view(['GET'])
def view_unanswered_questions(request):

    data = get_unanswered_questions()
    return Response(data)

###############################################################################


@api_view(['POST'])
def add_question(request):
    """
    {
            "email": "demouser1@gmail.com",
            "password":"pswd_1",
            "anonymous": "False",
            "question":"How to become 7 star on codechef",
            "tags":"competitive-programming,cp,dsa"
    }
    """
    serializer = AddQuestionSerializer(data=request.data)

    if serializer.is_valid():
        
        data = serializer.data
        
        email = data['email']
        password = data['password']
        question = data['question']
        tags = data['tags']
        anonymous = data['anonymous']
        
        check = checkUserForAddQuestion(email, password,question,tags,anonymous)
        
        if(check == True):
            return Response("Question added successfully")
        else:
            return Response("INVALID USER DATA")
    else:
        return Response("INVALID DATA", status=status.HTTP_400_BAD_REQUEST)

###############################################################################


@api_view(['POST'])
def add_answer(request):
    """
    {
            "username": "demouser1",
            "password":"pswd_1",
            "question":"How to be a full stack developer?",
            "answer":"Follow angela yu web development course on udemy."
    }
    """
    serializer = AddAnswerSerializer(data=request.data)

    if serializer.is_valid():
        data = serializer.data
        question = data['question']
        username = data['username']
        password = data['password']
        answer = data['answer']
        check = checkUser2(username, password,question,answer)
        if(check == True):
            #add_answer_db(question, username, answer)
            return Response("Answer added successfully")
        else:
            return Response("INVALID USER DATA")
    else:
        return Response("INVALID DATA", status=status.HTTP_400_BAD_REQUEST)

###############################################################################


@api_view(['POST'])
def view_specific_question(request):
    """
        {
                "question":"How to start with competetive programming?"
        }
        """
    serializer = ViewSpecificQuestionSerializer(data=request.data)
    if serializer.is_valid():
        question = serializer.data['question']
    data = get_specific_question(question)
    return Response(data)



###############################################################################

@api_view(['GET'])
def all_contributors(request):
    data=get_all_contributors()
    return Response(data, status=status.HTTP_200_OK)   

###############################################################################

@api_view(['GET'])
def all_users(request):
    data=get_all_users()
    return Response(data, status=status.HTTP_200_OK)   

###############################################################################

@api_view(['GET'])
def top5_contributors(request):
    data=get_top_5_contributors()
    return Response(data, status=status.HTTP_200_OK)     

###############################################################################

@api_view(['GET'])
def total_users_count(request):
    count=get_total_users_count()
    return Response(count, status=status.HTTP_200_OK)

###############################################################################

@api_view(['GET'])
def total_questions_count(request):
    count=get_total_questions_count()
    return Response(count, status=status.HTTP_200_OK)

###############################################################################

@api_view(['GET'])
def total_views_count(request):
    increase_views()
    count=get_total_views_count()
    return Response(count, status=status.HTTP_200_OK)

###############################################################################

@api_view(['POST'])
def upvote_question(request):
    """
    {
            "question":"Hello World !! Kush here :)"
    }
    """
    try:
        serializer = UpvoteQuestionSerializer(data=request.data)
        if serializer.is_valid():
            question = serializer.data['question']
            
            upvote_que(question)
            return Response(status=status.HTTP_200_OK)
        else:   
            return Response("INVALID SERIALIZED DATA", status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response("ERROR", status=status.HTTP_400_BAD_REQUEST)

###############################################################################

@api_view(['POST'])
def upvote_answer(request):
    """
    {
        "question":"Hello World !! Kush here :)",
        "answer":"answer 111"
    }
    """
    try:
        serializer = UpvoteAnswerSerializer(data=request.data)
        
        if serializer.is_valid():
            question = serializer.data['question']
            answer = serializer.data['answer']
            # print(question)
            # print(answer)
            upvote_ans(question, answer)  
            return Response(status=status.HTTP_200_OK)
        else:
            return Response("INVALID SERIALIZED DATA", status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response("ERROR", status=status.HTTP_400_BAD_REQUEST)
        
###############################################################################

@api_view(['GET'])
def all_tags(request):
    data=get_all_tags()
    return Response(data, status=status.HTTP_200_OK)   

###############################################################################

@api_view(['POST'])
def tagwise_question(request):
    """
    {
        "tag":"cp"
    }
    """
    try:
        
        print(1)
        serializer = SpecificTagSerializer(data=request.data)
        print(2)
        if serializer.is_valid():
            print(3)
            tag = serializer.data['tag']
            print(4)
            data = questionsByTag(tag)  
            print(5)
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response("INVALID SERIALIZED DATA", status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response("ERROR IN QUESTIONS BY TAG", status=status.HTTP_400_BAD_REQUEST) 

###############################################################################