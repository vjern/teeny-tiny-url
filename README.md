# URL Shortener API

Produce shortened versions of URLs (also called slugs).

## Available features

1. Register a new slug / shortened url with `POST /`
2. Access a slug and get redirected with `GET /<slug>`
3. List all slugs (for debug purposes) with `GET /list`

## Repo structure

`http` contains HTTP request examples as [http-request](https://www.jetbrains.com/help/idea/exploring-http-syntax.html) files. You can run them against a hostname with various IDE extensions (eg [VS Code Rest Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client)).

## Build & Run

This API is shipped with a Dockerfile.

You can build the Docker image & run it in a local container with:

```sh
make dev
# service is reachable on localhost:8080
# will stream logs
```

and also:

```sh
make logs # to show the full logs
make kill # stop the container
```

Or you can run the API directly with live reload (requires a virtual env):

```sh
make live
```

Then you can hit the following endpoints:

## Endpoints

Or check the examples in [http](http) (to be run with [VS Code Rest Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client)).

### Liveness

Check that your server is live by visiting http://localhost:8080.

```http
GET /
```

### Register a new slug

Add a new slug with

```http
POST /
Content-Type: application/json

{
  "url": "https://google.com"
}
```

Will return the slug key so you can use it next;

### Use a slug

```http
GET /<slug-key>
```

Will auto-redirect to the slug's registered url.

### List all slugs

To list all registered slugs, do:

```http
GET /list
```

## Rationale

### Edge cases

- Key collisions
- Invalid URLs (blank, no protocol etc)
- Race condition with same url at same timestamp