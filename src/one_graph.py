import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import font_manager, rc


rc('font', family='NanumGothic', size=17)

# 그래프 그리기 명령어 생성 함수
def make_plt_pie(make_plt):
    base_code = 'plt.pie(x = ratio, labels=labels, autopct="%.1f%%", startangle=260, counterclock=False '
    
    for i in make_plt:
        if make_plt[i] == False:
            continue
        else:
            jj = ', '+i + ' = ' + i
            base_code += jj
    base_code += ')'
    print(base_code)
    return base_code

def one_graph(ratio , labels , colors = None , wedgeprops = {'width': 0.7, 'edgecolor': 'w', 'linewidth': 3}):

    if len(ratio) != len(labels):
        print('ratio , labels The number must be the same')
        return 'ratio , labels The number must be the same'

    
    make_plt = dict()
    for i in ['colors' , 'wedgeprops' ]: #, 'wedgeprops'
        if eval(i) == None:
            make_plt[i] = False
        else:
            make_plt[i] = True
    
    plt_result = make_plt_pie(make_plt)
    fig = plt.figure(figsize=(12, 12))

    # 그래프 생성
    eval(plt_result)
    plt.legend(loc='lower center', ncol=len(labels))
    fig.savefig(fname='1.png', bbox_inches='tight', pad_inches=0)
    print('그래프가 생성되었습니다.')
    
