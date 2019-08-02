package com.manning.gia.todo.repository;

import java.util.List;

import com.manning.gia.todo.model.ToDoItem;

public interface ToDoRepository {
    List<ToDoItem> findAll();
    ToDoItem findById(Long id);
    Long insert(ToDoItem toDoItem);
    void update(ToDoItem toDoItem);
    void delete(ToDoItem toDoItem);
}
