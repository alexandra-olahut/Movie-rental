from entities import Operation, UpdateOperation
from repository import Repository

class ServiceUndo:

    def __init__(self, undo_stack, redo_stack):
        self.__undo_stack = undo_stack
        self.__redo_stack = redo_stack

    def undo(self):
        last_operation = self.__undo_stack.pop_op()
        redo_operation = last_operation
        undo_operation = last_operation.get_opposite_operation()
        undo_operation.execute()
        self.__redo_stack.push_op(redo_operation)

    def redo(self):
        redo_operation = self.__redo_stack.pop_op()
        redo_operation.execute()
        self.__undo_stack.push_op(redo_operation)

    def clear(self):
        self.__undo_stack.clear()