import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline

import plotly
import plotly.graph_objs as go
import plotly.offline as py
plotly.offline.init_notebook_mode(connected=True)

import warnings
warnings.filterwarnings('ignore')

# 读取csv文件
player_stats = pd.read_csv('2017-18_playerBoxScore.csv', parse_dates=['gmDate'])
team_stats = pd.read_csv('2017-18_teamBoxScore.csv', parse_dates=['gmDate'])
standings = pd.read_csv('2017-18_standings.csv', parse_dates=['stDate'])

# 提取相关数据
gs_gm_stats_2 = (team_stats[(team_stats['teamAbbr'] == 'GS') & 
                             (team_stats['seasTyp'] == 'Regular')]
                  .loc[:, ['gmDate', 
                           'team2P%', 
                           'team3P%', 
                           'teamPTS', 
                           'opptPTS']]
                  .sort_values('gmDate'))

# 添加比赛号码
gs_gm_stats_2['game_num'] = range(1, len(gs_gm_stats_2) + 1)

# 衍生出一个新的 “输赢” 列特征
win_loss = []
for _, row in gs_gm_stats_2.iterrows():

    # 如果76人队得分更多，判定为赢
    if row['teamPTS'] > row['opptPTS']:
        win_loss.append('W')
    else:
        win_loss.append('L')

# 添加输赢特征(winLoss)
gs_gm_stats_2['winLoss'] = win_loss

# Bokeh Libraries
from bokeh.plotting import figure, show
from bokeh.io import output_file
from bokeh.models import ColumnDataSource, CategoricalColorMapper, NumeralTickFormatter
from bokeh.layouts import gridplot

# Store the data in a ColumnDataSource
gm_stats_cds = ColumnDataSource(gs_gm_stats_2)

gs_gm_stats_2.head()

# Bokeh库
from bokeh.plotting import figure, show
from bokeh.io import output_file
from bokeh.models import ColumnDataSource, CategoricalColorMapper, NumeralTickFormatter
from bokeh.layouts import gridplot

# 步骤一：将数据储存在ColumnDataSource中
gm_stats_cds = ColumnDataSource(gs_gm_stats_2)

# 步骤二：生成一个静态的html文件
output_file('gs-gm-linked-selections.html',
            title='Golden State Percentages vs. Win-Loss')

# 创建CategoricalColorMapper，对win和loss分配特定颜色
win_loss_mapper = CategoricalColorMapper(factors = ['W', 'L'], palette=['Green', 'Red'])

# 自定义工具
toolList = ['lasso_select', 'tap', 'reset', 'save']

# 步骤三：配置图形界面
pctFig = figure(title='两分球得分率 % vs 3分球得分率 %, 2017-18 常规赛季',
                plot_height=400, plot_width=400, tools=toolList,
                x_axis_label='两分球得分率%', y_axis_label='3分球得分率%')

# 步骤四：采用圆点图绘制数据
pctFig.circle(x='team2P%', y='team3P%', source=gm_stats_cds, 
              size=12, color='blue')

# 将y轴标记变为百分比形式
pctFig.xaxis[0].formatter = NumeralTickFormatter(format='00.0%')
pctFig.yaxis[0].formatter = NumeralTickFormatter(format='00.0%')

# 创建一个与整体相关的图形
totFig = figure(title='团队得分 vs 对手得分, 2017-18 常规赛季',
                plot_height=400, plot_width=400, tools=toolList,
                x_axis_label='团队得分', y_axis_label='对手得分')

# 绘制正方形点图
totFig.square(x='teamPTS', y='opptPTS', source=gm_stats_cds, size=10,
              color=dict(field='winLoss', transform=win_loss_mapper))

# 创建图形布局
grid = gridplot([[pctFig, totFig]])

# 可视化展示
show(grid)