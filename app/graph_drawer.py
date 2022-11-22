import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import font_manager, rc


rc('font', family='NanumGothic', size=17)

# 그래프 그리기 명령어 생성 함수
def create_command(make_plt, graph_type= 'pie'):
    if graph_type == 'pie':
        base_code = 'plt.pie(x = ratio, labels=labels, autopct="%.1f%%", startangle=260, counterclock=False '
        
        for element in make_plt:
            if make_plt[element] == False:
                continue
            else:
                extra = f', {element} = {element}'
                base_code += extra
        base_code += ')'
    
    return base_code

def draw(ratio , labels , wedgeprops={'width': 0.7, 'edgecolor': 'w', 'linewidth': 3}):

    if len(ratio) != len(labels):
        print('ratio , labels The number must be the same')
        return 'ratio , labels The number must be the same'

    
    make_plt = dict()
    if 'wedgeprops' == None:
        make_plt['wedgeprops'] = False
        
    else:
        make_plt['wedgeprops'] = True
        graph_type = 'pie'       

    plt_result = create_command(make_plt, graph_type)
    fig = plt.figure(figsize=(12, 12))

    # 그래프 생성
    eval(plt_result)
    plt.legend(loc='lower center', ncol=len(labels))
    fig.savefig(fname='1.png', bbox_inches='tight', pad_inches=0)
    print('그래프가 생성되었습니다.')
    
