import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import font_manager, rc


rc('font', family='NanumGothic', size=17)

# 그래프 그리기 명령어 생성 함수
def create_command(wedgeprops, graph_type= 'pie'):
    if graph_type == 'pie':
        base_code = 'plt.pie(x = ratio, autopct="%.1f%%", startangle=260, counterclock=False, textprops={\'size\':30} '
        
        if wedgeprops != None:
            extra = f', wedgeprops = {wedgeprops}'
            base_code += extra
        base_code += ')'
    
    return base_code

def draw(ratio , labels , wedgeprops={'width': 0.7, 'edgecolor': 'w', 'linewidth': 3}):

    if len(ratio) != len(labels):
        print('ratio , labels The number must be the same')
        return 'ratio , labels The number must be the same'

    
    if 'wedgeprops' != None:
        graph_type = 'pie'       

    plt_result = create_command(wedgeprops, graph_type)
    fig = plt.figure(figsize=(12, 12))

    # 그래프 생성
    eval(plt_result)
    plt.legend(labels, loc='lower center', ncol=len(labels), fontsize=25)
    fig.savefig(fname='../data/images/1.png', bbox_inches='tight', pad_inches=0)
    print('그래프가 생성되었습니다.')
