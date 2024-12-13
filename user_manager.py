"""
Разработай систему управления учетными записями пользователей для небольшой компании
Компания разделяет сотрудников на обычных работников и администраторов. У каждого
сотрудника есть уникальный идентификатор (ID), имя и уровень доступа. Администраторы,
помимо обычных данных пользователей, имеют дополнительный уровень доступа и могут
добавлять или удалять пользователя из системы.

Требования:
1. Класс `User*: Этот класс должен инкапсулировать данные о пользователе: ID, имя и уровень
    доступа ('user' для обычных сотрудников).
2. Класс `Admin`: Этот класс должен наследоваться от класса `User`. Добавь дополнительный
    атрибут уровня доступа, специфичный для администраторов ('admin'). Класс должен также
    содержать методы `add_user` и `remove_user`, которые позволяют добавлять и удалять
    пользователей из списка (представь, что это просто список экземпляров `User`).
3. Инкапсуляция данных: Убедись, что атрибуты классов защищены от прямого доступа и
    модификации снаружи. Предоставь доступ к необходимым атрибутам через методы (например,
    get и set методы).
"""
class User:
    def __init__(self, name):
        self.__id = None
        self.__name = name
        self.__level = 'user'

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_level(self):
        return self.__level

    def _set_id(self, id):
        self.__id = id

    def _set_name(self, name):
        self.__name = name

    def _set_level(self, level):
        self.__level = level

    def info(self):
        print(f"name = {self.__name}, id = {self.__id}, level = {self.__level}")


class Admin(User):
    __user_list = []    # статический список всех пользователей

    @staticmethod
    def show_all_users():
        for user in Admin.__user_list:
            user.info()

    def __init__(self, name):
        super().__init__(name)
        self._set_level('admin')
        self.__sys_level = 'root'

    def info(self):
        print(f"name = {self.get_name()}, id = {self.get_id()}, level = {self.get_level()}, sys_level = {self.__sys_level}")

    @staticmethod
    def __user_is_exist(name):
        for user in Admin.__user_list:
            if user.get_name() == name:
                return True
        return False

    # находит уникальный номер для id
    @staticmethod
    def __get_max_id():
        max_id = 1
        for user in Admin.__user_list:
            if max_id <= user.get_id():
                max_id = user.get_id() + 1
        return max_id

    @staticmethod
    def __is_admin(user):
        if isinstance(user, Admin) and user in Admin.__user_list:
            if user.get_level() == 'admin' and user.__sys_level == 'root':
                return True
        return False

    # находим существующего админа, если администраторов ещё нет, создаём нового
    @staticmethod
    def get_admin():
        for user in Admin.__user_list:
            if Admin.__is_admin(user):
                return user
        admin = Admin('root')
        admin._set_id(Admin.__get_max_id())
        Admin.__user_list.append(admin)
        print(f"Создан администратор '{admin.get_name()}'")
        return admin

    def add_admin(self, name):
        if Admin.__is_admin(self):
            if Admin.__user_is_exist(name):
                print(f"Пользователь '{name}' уже существует")
                return None
            else:
                # создаём нового администратора
                admin = Admin(name)
                admin._set_id(Admin.__get_max_id())
                Admin.__user_list.append(admin)
                print(f"Администратор '{name}' добавлен")
                return admin
        else:
            print("*** hacking attempt detected ***")
            return None

    def add_user(self, name):
        if Admin.__is_admin(self):
            if Admin.__user_is_exist(name):
                print(f"Пользователь '{name}' уже существует")
                return None
            else:
                # создаём нового пользователя
                user = User(name)
                user._set_id(Admin.__get_max_id())
                Admin.__user_list.append(user)
                print(f"Пользователь '{name}' добавлен")
                return user
        else:
            print("*** hacking attempt detected ***")
            return None

    def remove_user(self, name):
        if Admin.__is_admin(self):
            if self.get_name() != name:
                i = 0
                removed = False
                while i < len(Admin.__user_list):
                    if Admin.__user_list[i].get_name() == name:
                        del Admin.__user_list[i]
                        print(f"Пользователь '{name}' удалён")
                        removed = True
                        continue
                    i += 1
                if not removed:
                    print(f"Пользователя '{name}' не существует")
            else:
                print("Администратор не может удалить сам себя!")
        else:
            print("*** hacking attempt detected ***")


def main():
    # получаем первого админа через статический метод класса Admin
    admin1 = Admin.get_admin()
    admin1.info()

    print("\nСоздаём второго админа")
    admin2 = admin1.add_admin("admin2")
    admin2.info()

    print("\nСоздаём простых пользователей")
    user1 = admin1.add_user('user1')
    user2 = admin1.add_user('user2')
    user1.info()
    user2.info()


    print("\nПроверяем разные способы доступа к защищенным и приватным методам")

    #print(len(admin1.__user_list))         ### not work
    #print(user1.__name)                    ### not work

    user1._set_name("ho-ho")                                        ### BAD CODE !!!
    print(f"всего пользователей: {len(admin1._Admin__user_list)}")  ### BAD HACK !!!
    admin1._set_level("super-admin")                                ### BAD CODE !!! hack admin1

    admin1.remove_user("user2")             ### not work - admin1 hacked
    admin2.remove_user("user2")

    print("\nСписок пользователей после эксперимента")
    Admin.show_all_users()


if __name__ == "__main__":
    main()
