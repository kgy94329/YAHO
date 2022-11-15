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

def one_graph(ratio , labels , colors = None , explode = None , wedgeprops = {'width': 0.7, 'edgecolor': 'w', 'linewidth': 3}):

    if len(ratio) != len(labels):
        print('ratio , labels The number must be the same')
        return 'ratio , labels The number must be the same'

    
    make_plt = dict()
    for i in ['colors' , 'explode' , 'wedgeprops' ]: #, 'wedgeprops'
        if eval(i) == None:
            make_plt[i] = False
        else:
            make_plt[i] = True
    
    # wedgeprops = {'width': 0.7}  #가운데 비어두기. linewidth 는 5만큼 떨어짐. 'edgecolor': 'w'  edgcolor 은 사이드 컬러가 w임.
    
    explodes = list()
    if explode != None:
        if len(explode) == 2:
            if explode[1] == 'defult':
                for i in range(len(ratio)):
                    explodes.append(explode[0])
            elif explode[1] == 'big':          ##큰거 튀어나오게.
                for i in range(len(ratio)):
                    if max(ratio) == ratio[i]:
                        explodes.append(explode[0] + 0.2)
                    else:
                        explodes.append(explode[0])

            elif explode[1] == 'small':  ##작은거 튀어나오게.
                for i in range(len(ratio)):
                    if min(ratio) == ratio[i]:
                        explodes.append(explode[0] + 0.2)
                    else:
                        explodes.append(explode[0])
            else:
                print('pop_out , Please choose None or big or small')
                return 'pop_out , Please choose None or big or small'
        else:
            for i in range(len(ratio)):
                explodes.append(explode[0])
    explode = explodes
    
    plt_result = make_plt_pie(make_plt)
    fig = plt.figure(figsize=(12, 12))

    # 그래프 생성
    eval(plt_result)
    plt.legend(loc='lower center', ncol=len(labels))
    fig.savefig(fname='1.png', bbox_inches='tight', pad_inches=0)
    print('그래프가 생성되었습니다.')
    


def manual():
    print('This is one_graph.py manual')
    print('The function one_graph parameter type is ratio , labels , explode , wedgeprops')
    print('ratio 는 그래프의 값을 의미 합니다. list 형식으로 넣습니다. 예 [30, 40 , 13 , 10]')
    print('label 은 각 값의 이름을 의미합니다. list 형식으로 넣습니다. 예 ["사과" , "배" , "수박" , "두리안"]')
    print('ratio 와 label 은 개수가 같아야 합니다.')
    print('colors 를 추가 하고 싶다면 컬러를 list 형식으로 ratio 개수와 같게 넣어야 합니다. 예 ["silver", "gold", "whitesmoke", "lightgray"]')
    print('wedgeprops 는 dict 형태로 넣습니다. 예 wedgeprops= {"width": 0.7, "edgecolor" : "w" , "linewidth": 2}')
    print('wedgeprops 의 width 는 가운데가 뚫린 원 형태의 그래프를 출력합니다. 값이 클수록 가운데 원이 작아집니다.')
    print('wedgeprops 의 edgecolor 은 그래프 가장자리 색깔을 의미 합니다. ')
    print('wedgeprops 의 linewidth 는 가장자리 색깔의 두깨를 의미합니다.')


# ratio = [34, 32, 12, 15]
# labels = ['Apple', 'Banana', 'Melon', 'Grapes' ]
# # colors = ['silver', 'gold', 'whitesmoke', 'lightgray']
# linewidth = 3
# edgecolor = 'w'
# width = 0.7



# one_graph(ratio = ratio ,labels =  labels ) #, wedgeprops = {'width': 0.7, 'edgecolor': 'w', 'linewidth': 5}



    
