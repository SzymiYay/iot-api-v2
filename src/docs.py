def get_description():
    return  """
This is a simple API for temperature measurements. It allows you to create users, devices and measurements.

## How to login
1. Create a user (see [Create a user](#create-a-user))
2. Login with the created user (see [Get a token](#get-a-token)), you will get an access token and a refresh token.
3. When the access token expires:
    1. Get a new access token with the refresh token (see [Refresh a token](#refresh-a-token))
    2. Login again (see [Get a token](#get-a-token))


## API documentation
1. [Base URL](#base-url)
2. [Authentication](#authentication)
    1. [Get a token](#get-a-token)
    2. [Refresh a token](#refresh-a-token)
3. [Users](#users)
    1. [Create a user](#create-a-user)
    2. [Get user details](#get-user-details)
    3. [Get user devices](#get-user-devices)
    4. [Create a device](#create-a-device)
    5. [Delete a device](#delete-a-device)
4. [Measurements](#measurements)
    1. [Create a measurement](#create-a-measurement)
    2. [Get a measurement](#get-a-measurement)
    3. [Get measurements](#get-measurements)
    4. [Get measurements by device](#get-measurements-by-device)

## Base URL
/api/v1

## Authentication

### Get a token

This API uses OAuth2 with password flow. You can get a token by sending a POST request to `/auth/login` with the following body: 

```json
{
    "username": "your_username",
    "password": "your_password"
}
```

The response will be a JSON object with the following structure:

```json
{
    "access_token": "your_access_token",
    "refresh_token": "your_refresh_token",
    "token_type": "bearer"
}
```

### Refresh a token

You can use the access token to access the API. The refresh token can be used to get a new access token when the current one expires. To do so, send a POST request to `/auth/token/refresh` with the following body:

```json
{
    "username": "your_username",
    "password": "your_password",
}
```

The response will be a JSON object with the following structure:

```json
{
    "refresh_token": "your_refresh_token",
}
```

## Users

### Create a user

To create a user, send a POST request to `/auth/signup` with the following body:

```json
{
    "username": "your_username",
    "email": "your_email",
    "password": "your_password"
}
```

### Get user details

To get the details of the current user, send a GET request to `/users/profile`. The response will be a JSON object with the following structure:

```json
{
    "username": "your_username",
    "email": "your_email"
}
```

### Get user devices

To get the devices of the current user, send a GET request to `/users/devices`. The response will be a JSON object with the following structure:

```json
[
    {
        "id": 1,
        "name": "your_device_name",
        "user_id": 1
    }
]
```

### Create a device

To create a device, send a POST request to `/users/devices` with the following body:

```json
{
    "name": "your_device_name"
}
```

### Delete a device

To delete a device, send a DELETE request to `/users/devices/{device_id}` with the following body:

```json
{
    "device_id": 1
}
```

## Measurements

### Create a measurement

To create a measurement, send a POST request to `/measurements` with the following body:

```json
{
    "temperature": 20,
    "device_id": 1
}
```

### Get a measurement

To get a measurement, send a GET request to `/measurements/{measurement_id}`. The response will be a JSON object with the following structure:

```json
{
    "temperature": 20,
    "time_created": "2021-01-01T00:00:00+00:00",
    "device_id": 1
}
```

### Get measurements

To get all measurements, send a GET request to `/measurements`. The response will be a JSON object with the following structure:

```json
[
    {
        "temperature": 20,
        "time_created": "2021-01-01T00:00:00+00:00",
        "device_id": 1
    }
]
```

### Get measurements by device

To get all measurements of a device, send a GET request to `/measurements/devices/{device_id}`. The response will be a JSON object with the following structure:

```json
[
    {
        "temperature": 20,
        "time_created": "2021-01-01T00:00:00+00:00",
        "device_id": 1
    }
]
"""
