from abc import ABC, abstractmethod

class IUserInterface(ABC):
    @abstractmethod
    def get_input(self, prompt: str) -> str: pass

    @abstractmethod
    def show_message(self, message: str): pass

    @abstractmethod
    def show_error(self, error: str): pass

class ConsolePresentation(IUserInterface):
    def get_input(self, prompt: str) -> str:
        return input(f"> {prompt}: ")

    def show_message(self, message: str):
        print(f"\n[INFO]: {message}")

    def show_error(self, error: str):
        print(f"\n[ERROR]: {error}")