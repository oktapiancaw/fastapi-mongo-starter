# Testing

## Modules - test/test_module.py
This testing is intended for modules that are in the service

**test_mongo_connection**

This is a test function that verifies the connection to a MongoDB server using the `MainMongo` class. It:

1. Creates a `MainMongo` instance.
2. Tries to connect to the MongoDB server.
3. Asserts that the connection was successful by checking for the presence of a `_client` attribute and executing the `ismaster` command.
4. Regardless of the outcome, closes the connection in the `finally` block.
5. Asserts that the connection is closed by checking that the `_client` attribute is no longer present.

This test ensures that the `MainMongo` class can establish and close a connection to the MongoDB server correctly.

**test_post_service**

This is a test function for the `PostService` class. It tests the following scenarios:

1. Adding a new post and verifying it's not `None`.
2. Retrieving the added post by its ID and verifying it's not `None`.
3. Retrieving all posts and verifying there's at least one post.
4. Updating the post's title and content, and verifying the update was successful.
5. Retrieving the updated post and verifying its title has changed.
6. Deleting the post and verifying the deletion was successful.

The test function uses assertions to ensure each step completes as expected.

## Base API - test/test_main.py
This testing is intended for the basics of service

**test_service_status**

This is a test function that checks if a service is running correctly by sending a GET request to the root URL ("/") and asserting that the response status code is 200 (OK).

## Post API - test/test_post.py
This testing is intended for the post api

**test_creation_post**

This is a test function `test_creation_post` that tests the creation, retrieval, and deletion of a post using the `client` object, which is likely a test client for a FastAPI application.

Here's a succinct breakdown of what the code does:

1. Creates a new post by sending a POST request to `/posts` with a JSON payload from `SAMPLE[0]`.
2. Verifies that the response status code is 201 (Created) and that the response data is valid according to the `Post` model.
3. Retrieves the created post by sending a GET request to `/posts/<id>`, where `<id>` is the ID of the newly created post.
4. Verifies that the response status code is 200 (OK) and that the response data matches the original post data.
5. Deletes the post by sending a DELETE request to `/posts/<id>`.
6. Verifies that the response status code is 200 (OK).

In summary, this test function exercises the CRUD (Create, Read, Delete) operations for a post resource in the application.

**test_multiple_post**

This code snippet is a test function that tests the flow of creating, getting, deleting, and getting all posts in a web application. 

Here's a breakdown of what the code does:

1. It sends a POST request to the `/posts` endpoint with a JSON payload containing the data of a sample post. It expects the response status code to be 201 (indicating successful creation of the post).
2. It validates the response data using the `Post.model_validate()` function.
3. It retrieves the payload from the response JSON and assigns it to the `payload` variable.
4. It sends a GET request to the `/posts` endpoint to retrieve all posts. It expects the response status code to be 200 (indicating successful retrieval of the posts).
5. It retrieves the total count of posts from the response JSON and assigns it to the `total` variable.
6. It sends a DELETE request to the `/posts/{id}` endpoint with the ID of the post retrieved earlier. It expects the response status code to be 200 (indicating successful deletion of the post).
7. It sends another GET request to the `/posts` endpoint to retrieve all posts again. It expects the response status code to be either 200 or 404 (indicating successful retrieval of the updated list of posts or not finding any posts).
8. If the response status code is 200, it asserts that the total count of posts in the response JSON is different from the `total` variable.

Overall, this test function verifies that the application correctly handles the creation, retrieval, deletion, and updating of posts in the database.


**test_update_post**

This is a test function `test_update_post` that simulates the following workflow:

1. Creates a new post using `POST /posts` with sample data `SAMPLE[0]`.
2. Updates the created post using `PUT /posts/<id>` with sample data `SAMPLE[1]`.
3. Retrieves the updated post using `GET /posts/<id>` and verifies its title has changed.
4. Deletes the post using `DELETE /posts/<id>`.

The test asserts that each step returns the expected HTTP status code and that the post data is valid according to the `Post` model.