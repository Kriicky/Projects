package com.example.todo;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.atomic.AtomicLong;

import org.springframework.stereotype.Repository;

@Repository
public class TaskRepository {

    private final List<Task> tasks = new ArrayList<>();
    private final AtomicLong idGenerator = new AtomicLong(1);

    public List<Task> findAll() {
        return new ArrayList<>(tasks);
    }

    public Optional<Task> findById(Long id) {
        return tasks.stream().filter(t -> t.id().equals(id)).findFirst();
    }

    public Task save(Task task) {
        if (task.id() == null) {
            Long newId = idGenerator.getAndIncrement();
            Boolean completed = task.completed() != null ? task.completed() : false;
            Task newTask = new Task(newId, task.title(), completed);
            tasks.add(newTask);
            return newTask;
        } else {
            tasks.removeIf(t -> t.id().equals(task.id()));
            tasks.add(task);
            return task;
        }
    }

    public void deleteById(Long id) {
        tasks.removeIf(t -> t.id().equals(id));
    }
}
