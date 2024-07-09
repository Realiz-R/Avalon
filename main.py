import re

def init():
    try:
        # Открываем файл для чтения
        with open('main.avl', 'r', encoding='utf-8') as file:
            # Читаем содержимое файла в переменную text
            text = file.read()

        return text  # Возвращаем text из функции

    except FileNotFoundError:
        print("Файл 'main.avl' не найден.")
        return None

    except PermissionError:
        print("Ошибка доступа к файлу 'main.avl'. Проверьте права доступа.")
        return None

    except UnicodeDecodeError:
        print("Ошибка декодирования файла 'main.avl'. Проверьте формат файла.")
        return None

    except IOError as e:
        print(f"Произошла ошибка ввода-вывода: {e}")
        return None

    except Exception as e:
        print(f"Произошла неизвестная ошибка: {e}")
        return None

variables = {}

def main():
    # Читаем содержимое файла
    text = init()
    if text:
        # Разбиваем текст на строки
        lines = text.split('\n')
        
        # Регулярные выражения для обнаружения переменных, команд print(), input() и условных операторов
        var_pattern = re.compile(r'^\s*([a-zA-Z_]\w*)\s*=\s*(.+)$')
        print_pattern = re.compile(r'^\s*print\((.+)\)\s*$')
        input_pattern = re.compile(r'^\s*input\((.+)\)\s*$')
        if_pattern = re.compile(r'^\s*if\s+(.+):\s*$')
        elif_pattern = re.compile(r'^\s*elif\s+(.+):\s*$')
        else_pattern = re.compile(r'^\s*else:\s*$')
        # Для отслеживания текущего состояния выполнения условных операторов
        executing = True
        skip_else = False
        
        # Выполняем каждую строку как команду
        for line in lines:
            command = line.strip()
            if command:
                try:
                    # Проверяем, является ли команда инициализацией переменной
                    var_match = var_pattern.match(command)
                    if var_match:
                        var_name = var_match.group(1)
                        expression = var_match.group(2)
                        if executing:
                            variables[var_name] = eval(expression, {}, variables)
                        continue
                    
                    # Проверяем, является ли команда print()
                    print_match = print_pattern.match(command)
                    if print_match:
                        if executing:
                            print_expression = print_match.group(1)
                            eval(f'print({print_expression})', {}, variables)
                        continue
                    
                    # Проверяем, является ли команда input()
                    input_match = input_pattern.match(command)
                    if input_match:
                        if executing:
                            input_expression = input_match.group(1)
                            user_input = input(eval(input_expression, {}, variables))
                            variables['_'] = user_input  # Временная переменная для хранения ввода
                        continue
                    
                    # Проверяем, является ли команда if
                    if_match = if_pattern.match(command)
                    if if_match:
                        condition = if_match.group(1)
                        executing = eval(condition, {}, variables)
                        skip_else = executing
                        continue
                    
                    # Проверяем, является ли команда elif
                    elif_match = elif_pattern.match(command)
                    if elif_match:
                        if not skip_else:
                            condition = elif_match.group(1)
                            executing = eval(condition, {}, variables)
                            skip_else = executing
                        else:
                            executing = False
                        continue
                    
                    # Проверяем, является ли команда else
                    else_match = else_pattern.match(command)
                    if else_match:
                        executing = not skip_else
                        continue
                    
                    # Если команда не распознана
                    if executing:
                        print(f"Неподдерживаемая команда: {command}")
                
                except Exception as e:
                    print(f"Произошла ошибка при выполнении команды '{command}': {e}")

# Пример использования
if __name__ == "__main__":
    main()