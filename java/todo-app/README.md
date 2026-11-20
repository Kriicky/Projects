# Spring Boot 4 To-Do Application

A simple to-do app built with Spring Boot 4 and Java 21. It provides a REST API and a basic HTML frontend, and stores tasks in memory.

> **Note:** Tasks are kept in memory only, so they're cleared every time the app restarts.

## Prerequisites

- **Java 21** (JDK)
- **Maven 3.8+**

Check what you already have:

```bash
java -version
mvn -version
```

### Installing Java 21 and Maven

| Platform              | Java 21                                | Maven                       |
|-----------------------|----------------------------------------|-----------------------------|
| Ubuntu / Debian       | `sudo apt install openjdk-21-jdk`      | `sudo apt install maven`    |
| Fedora / RHEL         | `sudo dnf install java-21-openjdk-devel` | `sudo dnf install maven`  |
| macOS (Homebrew)      | `brew install openjdk@21`              | `brew install maven`        |
| Windows (Chocolatey)  | `choco install openjdk21`              | `choco install maven`       |
| Windows (Scoop)       | `scoop install openjdk21`              | `scoop install maven`       |

On Ubuntu/Debian, run `sudo apt update` first. On macOS, Homebrew's `openjdk@21` isn't linked automatically. Follow the `brew info openjdk@21` instructions, or set `JAVA_HOME`, so `java -version` reports 21.

## Getting Started

```bash
git clone https://github.com/Kriicky/Projects.git
cd Projects/java/todo-app
```

### Run in development

```bash
mvn spring-boot:run
```

### Build and run the JAR

```bash
mvn clean package
java -jar target/todo-app-0.0.1-SNAPSHOT.jar
```

Once it starts, open **http://localhost:8080** in your browser for the frontend. The API is served from the same address.

To use a different port:

```bash
mvn spring-boot:run -Dspring-boot.run.arguments=--server.port=9090
# or
java -jar target/todo-app-0.0.1-SNAPSHOT.jar --server.port=9090
```

## API Reference

| Method | Endpoint      | Description                        |
|--------|---------------|------------------------------------|
| GET    | `/tasks`      | List all tasks                     |
| GET    | `/tasks/{id}` | Get a single task                  |
| POST   | `/tasks`      | Create a task                      |
| PUT    | `/tasks/{id}` | Update a task (e.g. mark complete) |
| DELETE | `/tasks/{id}` | Delete a task                      |

A task looks like this:

```json
{ "id": 1, "title": "Buy groceries", "completed": false }
```

### Examples

The examples use `curl` on macOS/Linux. On Windows, run them in Git Bash or WSL, or call `curl.exe` from PowerShell.

**Create a task**
```bash
curl -X POST http://localhost:8080/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy groceries"}'
```

**List all tasks**
```bash
curl http://localhost:8080/tasks
```

**Get one task**
```bash
curl http://localhost:8080/tasks/1
```

**Mark a task as completed**
```bash
curl -X PUT http://localhost:8080/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy groceries","completed":true}'
```

**Delete a task**
```bash
curl -X DELETE http://localhost:8080/tasks/1
```

## Running Tests

```bash
mvn test
```

The tests use MockMvc to exercise the REST controller without starting a full server.

## Project Structure

```
todo-app/
├── pom.xml
├── src/
│   ├── main/
│   │   ├── java/com/example/todo/
│   │   │   ├── TodoApplication.java      # Spring Boot entry point
│   │   │   ├── Task.java                 # Task record
│   │   │   ├── TaskRepository.java       # In-memory repository
│   │   │   └── TaskController.java       # REST controller
│   │   └── resources/static/
│   │       └── index.html                # Frontend
│   └── test/
│       └── java/com/example/todo/
│           └── TaskControllerTest.java   # MockMvc tests
└── README.md
```

## Spring Boot 4 Notes

This project targets Spring Boot 4.0. If you're coming from Spring Boot 3, note these differences:

- `spring-boot-starter-webmvc` replaces `spring-boot-starter-web`
- `spring-boot-starter-webmvc-test` is used for tests
- `@AutoConfigureMockMvc` is imported from `org.springframework.boot.webmvc.test.autoconfigure`
- Jackson 3 is used, under the `tools.jackson.databind` package
- `@MockitoBean` replaces the removed `@MockBean`

## License

Licensed under the GNU General Public License. See [LICENSE](LICENSE) for details.
