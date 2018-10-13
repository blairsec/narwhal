Host challenge servers with Docker

## Requests
All request bodies should be content-type `application/json`.

## Responses
### Instances
Note: The response contains a field for each instance.

|name|type|
|----|----|
|`{name}`|[instance](#instance)|

### Instance

|name|type|
|----|----|
|image|string|
|status|string|
|labels|string|

## Routes
* [List instances](#list-instances)
* [Get an instance](#get-an-instance)
* [Create an instance](#create-an-instance)
* [Update an instance](#update-an-instance)
* [Delete an instance](#delete-an-instance)

### List instances
#### `GET /instances`
#### Responses

|code|content|
|----|-------|
|200|[instances](#instances)|

### Get an instance
#### `GET /instances/{name}`
#### Responses

|code|content|
|----|-------|
|200|[instance](#instance)|
|400|`"Bad request", "Invalid name."`|

### Create an instance
#### `POST /instances`
#### Request

|name|type|required|requirements|
|----|----|--------|------------|
|repo|string|yes|repo must exist|
|tag|string|yes|repo must have tag|

#### Responses

|code|description|
|----|-------|
|200|none|
|500|`"Internal server error", "Unable to create instance."`|

### Update an instance
#### `PATCH /instances/{name}`
#### Request

|name|type|required|requirements|
|----|----|--------|------------|
|action|string|yes|one of `"start", "stop", "restart"`|

#### Responses

|code|content|
|----|-------|
|200|none|
|400|`"Bad request", "Invalid name."`|
|400|`"Bad request", "Invalid JSON data."`|

### Delete an instance
#### `DELETE /instances/{name}`
#### Responses

|code|content|
|----|-------|
|200|none|
|400|`"Bad request", "Invalid name."`|