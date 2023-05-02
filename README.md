# CS 515-A Spring 2023 - Project 3 - Web Forum

## Submitted By

- Name: Anirudh Chintha
- Email: achintha@stevens.edu

- Name: Pooja Vaijanath Mule
- Email: pmule@stevens.edu

- Name: KavyaSri Thalluri
- Email: kthallur@stevens.edu

## Github URL

- https://github.com/anirudhchintha95/web-forum

## Description

This project uses `Flask` for backend that serves a variety of JSON REST API endpoints that could be used to run a web forum.

## Steps for installation

### Mac

- Install python and mongodb
- Make sure your mongodb server is running
- Run `python3 -m venv venv`. This creates a virtual environment
- Run `. venv/bin/activate`. This will activate your python virtual environment
- Run `pip3 install -r requirements.txt`

### Ubuntu

- Just run setup.sh and it should setup the environment for you

## Hours spent on project

- Anirudh Chintha: 18 hours
- Pooja Vaijanath Mule: 18 hours
- KavyaSri Thalluri: 18 hours

## How the code was tested
- We first manually tested the code going through each endpoint and making sure that it works in all the use cases.
- Once we started pushing the code to github, we used github actions to run the tests.
- We used postman collections to test the endpoints and make sure that they work as expected.
- We used github workflows to initially simulate the environment of the gradescope and ran postman collection tests.
- We then ran the tests on the gradescope when it went up and made sure that all the tests passed.

## Unresolved bugs or issues
- None

## Example of difficult issue or bug and how it was resolved
- Getting gradescope to accept our submission was a bit difficult. 
- We had to manually seup mongodb and its requirements on the gradescope environment.
- We faced an issue where the gradescope was not able to run the tests on the postman collection because mongodb was not running.
- We later figured out that we had to run mongodb using `/usr/bin/mongod --fork --logpath /var/log/mongodb/mongod.log --config /etc/mongod.conf` since gradescope used dumb-init environment.
## Extensions implemented
### User and user keys
- This will help us create a user and tag him to all the posts that he creates.
- Authentication is done by keeping the `user_key` in the header with the value of user's `key` in the request.
- Because of this addition, posts now will have an extra user key if its created by a user using the above said authentication. The response of post includes all the keys described in the project along with user key which includes

```
- `id` is be an integer
- `timestamp` is an ISO 8601 timestamp in UTC
- `username` is the username of the user
- `firstname` is the first name of the user
```
### User Profiles
- This will create endpoints to edit the user
- It also adds/updates endpoints that will add/edit `firstname` to the user.

### User-Based queries
- This adds an endpoint to get all the posts created by a user.

### Fulltext search
- This adds an endpoint to search for posts based on the text in the post.

### Persistence
- We used `mongodb` to store all the users and posts data.
- MongoDB is a document based database that stores data in JSON format.
- It inherently provides `_id` which we used as a unique `key` for each user and post.
- We also used counters to generate unique `int:<id>` for users and posts.

## Endpoints
### Endpoint #1: create a user with `POST /users/create`
A POST request to `/users/create` will have a body consisting of a JSON object with a following string-valued fields.

- `username`: a string that is the username of the user to create. Considered to be unique
- `password`: a string that is the password of the user to create. This is hashed and stored for future purposes.
- `firstname`: a string that is the first name of the user to create. Non-unique field.

The endpoint requires all the 3 fields to be present in the request body. If any of the fields are missing, the endpoint should return a 400 status code.

This will return a JSON object with 5 fields:

- `id` is be an integer
- `key` is a long, unique random string (which is used to later edit the user or authenticate)
- `timestamp` is an ISO 8601 timestamp in UTC
- `username` is the username of the user
- `firstname` is the first name of the user

### Endpoint #2: get a user with `GET /users/{{id}}`
A GET request to `/users/{{id}}` returns the user with the given id. The response is a JSON object with the following fields:

- `id` is be an integer
- `timestamp` is an ISO 8601 timestamp in UTC
- `username` is the username of the user
- `firstname` is the first name of the user

NOTE: This endpoint requires authentication. Create a user first, get his unique `key` and add that to the header of the request as `user_key`.

### Endpoint #3: edit a user with `PUT /users/edit`
A PUT request to `/users/edit` will have a body consisting of a JSON object with at least one of the following string-valued fields.

- `username`: a string that is the username of the user to update. Considered to be unique
- `password`: a string that is the password of the user to update. This is hashed and stored for future purposes.
- `firstname`: a string that is the first name of the user to update. Non-unique field.

The endpoint requires at least one of the 3 fields to be present in the request body. If none of the fields are present, the endpoint should return a 400 status code.

Also, the endpoint requires at least one field to have changed if all the 3 are submitted. Else, it should return a 400 status code.

If the fields are individually sent, these are the validations

- If the username is not unique or empty, the endpoint should return a 400 status code.
- If the password is empty or same, the endpoint should return a 400 status code.
- If the firstname is empty, the endpoint should return a 400 status code.

This will return a JSON object with 5 fields:

- `id` is be an integer
- `key` is a long, unique random string (which is used to later edit the user or authenticate)
- `timestamp` is an ISO 8601 timestamp in UTC
- `username` is the username of the user
- `firstname` is the first name of the user

### Endpoint #4: get a user's posts with `GET /users/{{id}}/posts`
A GET request to `/users/{{id}}/posts` returns the user's posts whose id is the given id. The response is an array of JSON object with the following fields:

If user's id is not related to any user, it raises a `404` error

- `id` is be an integer
- `timestamp` is an ISO 8601 timestamp in UTC
- `msg` is the message of the post
- `user` is the user who created it. If post is created anonymously, then it returns null. Else it will return the user object with the following fields
    - `id` is be an integer
    - `timestamp` is an ISO 8601 timestamp in UTC
    - `username` is the username of the user
    - `firstname` is the first name of the user

### Endpoint #5: get all posts with `GET /post`
A GET request to `/post` returns the all the posts. The response is an array of JSON object with the following fields:

- `id` is be an integer
- `timestamp` is an ISO 8601 timestamp in UTC
- `msg` is the message of the post
- `user` is the user who created it. If post is created anonymously, then it returns null. Else it will return the user object with the following fields
    - `id` is be an integer
    - `timestamp` is an ISO 8601 timestamp in UTC
    - `username` is the username of the user
    - `firstname` is the first name of the user

### Endpoint #6: get posts that contains search term with `GET /post/query/search`
A GET request to `/post/query/search` returns the all the posts which contains a search item. The keyword required is `search` and should be added to the query params.

If `search` is not present or empty, it raises a `400` error

The response is an array of JSON object with the following fields:

- `id` is be an integer
- `timestamp` is an ISO 8601 timestamp in UTC
- `msg` is the message of the post
- `user` is the user who created it. If post is created anonymously, then it returns null. Else it will return the user object with the following fields
    - `id` is be an integer
    - `timestamp` is an ISO 8601 timestamp in UTC
    - `username` is the username of the user
    - `firstname` is the first name of the user

### Endpoint #7: changes to create a post with `POST /post`
- The baseline behaviour works as expected.
- To make sure we associate a post to a user, we added a `user_key` in the header of the request.
- This assigns user to the post and the post later can only be deleted by this user and no one else.
- Anonymous posts are still allowed and can be deleted by anyone irrespective of `user_key` in the header.

### Endpoint #8: changes to delete a post with `DELETE /post/<post_counter_id>/delete/<id>`
- The baseline behaviour works as expected.
- If a user creates a post, only he can delete.
- If the user who did not create the post tries to delete it, then we throw a `404` error


## Detailed test summary for our extensions

### Extension 1: User and user keys
1. Endpoint is provided to create user as user/create
2. The endpoint requires: `username`, `password`, `firstname`
3. `user_key` is generated for every user created in order to associate to identify the user by this unique key.
4. Each post can be associated with the `user_key` of the user who created the post.
5. Posts can still be created anonymously without providing the `user_key` in the header.
6. If a post has an associated user, then on creation, details of both the post and user are returned.
7. If a post is created anonymously, then only the post details are returned.
8. If a post is created anonymously, then any user can delete it.
9. If a post is created by a user, then the `user_key` of the user who created the post is required in the header parameter for deletion.
### Extension 2: User profiles
1. Get User<br>
    a. This extension returns the user whose `id` is provided in the endpoint.<br>
    b. Endpoint: user/{{id}}<br>
    c. The `user_key` of the user requesting the user is provided in the header parameter.<br>
    d. Validation is implemented where if the user `id` does not exist in the DB, then a relevant error message is returned with a status code of 404.<br>
    e. If `user_key` is not provided in the header, then forbidden error message is returned with a status code of 403.<br>
2. Edit User<br>
    a. This extension edits the user whose `user_key` is provided in the header.<br>
    b. Endpoint: user/edit<br>
    c. The entire body is not required to be passed again to update the user. Only the fields that need to be updated can be passed in the body.<br>
    d. Validation is in place if no fields are passed in the body, then a relevant error message is returned with a status code of 400.<br>
    e. If the fields provided have no changes compared to the old values, then user is shown a relevant message asking for at least one field to be changed to edit the user.<br>


### Extension 3: User-based range queries
1. This extension returns all the posts of the user whose `id` is provided in the endpoint.
Example: http://127.0.0.1:5000/post/{{id}}
2. The `user_key` of the user requesting the posts is provided in the header parameter.
3. The request can also be made anonymously without providing the key in the headers.
4. Validation is implemented where if the user `id` for which the posts are being requested does not exist in the DB, then a relevant error message is returned with a status code of 404.
### Extension 4: Fulltext search
1. Users can provide the text in the `search` query parameter to search for the posts containing the text.
2. The search is case insensitive.
3. The search returns all the posts where the `msg` contains the text provided in the `search` query parameter.
4. No posts are returned if the `search` query parameter is not provided.
5. Empty array is returned if no posts are found with the given `search` term.

### Extension 5: Persistence
1. We have used MongoDB as our database. We have created a database named `web-forum` and collections named `users`, `posts`
2. Each of the write requests made to the server are stored in the database.
3. The Postman collection is written in such a way that it takes into account the previous requests made to the server and uses the data from the previous requests to make the next request.
4. The test cases running on postman collections ensure proper checks to see if the data is being stored in the database correctly.