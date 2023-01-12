

def func_sum(**kwargs):
    ret = int(kwargs['number_1']) + int(kwargs['number_2'])
    # 打印结果
    kwargs['TextCtrl'].AppendText('\n结果为:{0}'.format(ret))


def func_mul(**kwargs):
    ret = int(kwargs['number_1']) * int(kwargs['number_2'])
    # 打印结果
    kwargs['TextCtrl'].AppendText('\n结果为:{0}'.format(ret))
