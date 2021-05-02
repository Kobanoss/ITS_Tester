import json
import hashlib


def _json_import():
    try:
        with open("data_file.json", "r") as file:
            data = json.load(file)
        return data
    except IOError:
        ('File is not exist')
    except json.decoder.JSONDecodeError:
        ('File is empty')
        return {}


def _json_export(data):
    with open("data_file.json", "w") as file:
        json.dump(data, file)


def _get_hash(obj):
    return hashlib.sha1(str(obj).encode()).hexdigest()


def encode_function(func):
    def __wrapper(*args, **kwargs):
        global testing_dict
        testing_dict = _json_import()

        result_hash = _get_hash(list(func(*args, **kwargs)))

        if func.__name__ not in testing_dict:
            value = [[*args, *kwargs], result_hash]
            testing_dict.update({func.__name__: [value]})
        else:
            for value_pack in testing_dict[func.__name__]:
                if [*args, *kwargs] in value_pack:
                    raise Exception('\n'
                                    'These input args already exist\n'
                                    'Try manually delete them\n'
                                    'Or change args')

            value = testing_dict[func.__name__]
            value.append([[*args, *kwargs], result_hash])
            testing_dict.update({func.__name__: value})

        _json_export(testing_dict)
        print(f'#Test exported: "{func.__name__}" \n'
              '#With args:', *args, **kwargs)

    return __wrapper


def _checker(name, run):
    return testing_dict[name][run][0], testing_dict[name][run][1]


def test(func):
    def __wrapper(*args, **kwargs):
        global testing_dict
        testing_dict = _json_import()

        print('Testing...')
        print(f'Testing function: {func.__name__}()')

        for run in range(len(testing_dict[func.__name__])):
            print(f'\nTest #{run + 1}')

            input_list, predicted_hash, = _checker(func.__name__, run)
            result = list(func(*args, **kwargs))
            result_hash = _get_hash(result)

            print('\n',
                  'Input: ', *input_list, '\n',
                  'Testing Function Result: ', *result, '\n',
                  'Testing Function Hash: ', result_hash, '\n',
                  'Predicted Hash: ', predicted_hash, '\n')

            if predicted_hash != result_hash:
                print('#Test failed')
                break
            print('#Success')

    return __wrapper
