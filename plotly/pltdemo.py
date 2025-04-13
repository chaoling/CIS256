import plotly.graph_objects as go
import plotly.express as px

def demo1():
        # Add data
    month = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
            'August', 'September', 'October', 'November', 'December']
    high_2000 = [32.5, 37.6, 49.9, 53.0, 69.1,
                75.4, 76.5, 76.6, 70.7, 60.6, 45.1, 29.3]
    low_2000 = [13.8, 22.3, 32.5, 37.2, 49.9,
                56.1, 57.7, 58.3, 51.2, 42.8, 31.6, 15.9]
    high_2007 = [36.5, 26.6, 43.6, 52.3, 71.5,
                81.4, 80.5, 82.2, 76.0, 67.3, 46.1, 35.0]
    low_2007 = [23.6, 14.0, 27.0, 36.8, 47.6,
                57.7, 58.9, 61.2, 53.3, 48.5, 31.0, 23.6]
    high_2014 = [28.8, 28.5, 37.0, 56.8, 69.7,
                79.7, 78.5, 77.8, 74.1, 62.6, 45.3, 39.9]
    low_2014 = [12.7, 14.3, 18.6, 35.5, 49.9,
                58.0, 60.0, 58.6, 51.7, 45.2, 32.2, 29.1]

    fig = go.Figure()
    # Create and style traces
    fig.add_trace(go.Scatter(x=month, y=high_2014, name='High 2014',
                            line=dict(color='firebrick', width=4)))
    fig.add_trace(go.Scatter(x=month, y=low_2014, name='Low 2014',
                            line=dict(color='royalblue', width=4)))
    fig.add_trace(go.Scatter(x=month, y=high_2007, name='High 2007',
                            line=dict(color='firebrick', width=4,
                                    dash='dash')  # dash options include 'dash', 'dot', and 'dashdot'
                            ))
    fig.add_trace(go.Scatter(x=month, y=low_2007, name='Low 2007',
                            line=dict(color='royalblue', width=4, dash='dash')))
    fig.add_trace(go.Scatter(x=month, y=high_2000, name='High 2000',
                            line=dict(color='firebrick', width=4, dash='dot')))
    fig.add_trace(go.Scatter(x=month, y=low_2000, name='Low 2000',
                            line=dict(color='royalblue', width=4, dash='dot')))

    # Edit the layout
    fig.update_layout(title='Average High and Low Temperatures in New York',
                    xaxis_title='Month',
                    yaxis_title='Temperature (degrees F)')
    fig.show()


def line_graph():
    df_stocks = px.data.stocks()
    fig1 = px.line(df_stocks, x='date', y='GOOG', labels = {'x': "Date", 'y': "Price"})
    fig1.show()
    fig2 = px.line(df_stocks, x='date', y=['GOOG','AAPL'],
                labels={'x': "Date", 'y': "Price"}, title='Apple vs. GOOGLE')
    fig2.show()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_stocks.date, y=df_stocks.AAPL, mode='lines', name="Apple"))
    fig.add_trace(go.Scatter(x=df_stocks.date, y=df_stocks.AMZN, mode='lines+markers', name="Amazon"))
    fig.add_trace(go.Scatter(x=df_stocks.date, y=df_stocks.GOOG, mode='lines+markers', name="Google",
                                line=dict(color='teal', width=2, dash='dashdot')))

    fig.update_layout(title='Stock Price Data 2018-2020', xaxis_title="Date", yaxis_title='Price',
    xaxis=dict(showline=True, showgrid=False, showticklabels=True, linecolor='rgb(255,200,123)',
    linewidth=2,ticks='outside', tickfont=dict(family='Arial', size=12, color='rgb(42,82,121)'),),
    yaxis=dict(showgrid=False, zeroline=False, showline=True, showticklabels = False),
    autosize=False, margin=dict(autoexpand=False, l=100, r=20, t=110, ),
    showlegend=True, plot_bgcolor='silver')
    fig.show()


#Bar Charts
def bar_chart():
    px.bar(x=["a", "b", "c"], y=[1, 3, 2]).show()
    df_us = px.data.gapminder().query("country == ['United States','Canada']")
    #print(type(df_us),df_us.hist)
    px.bar(df_us,x = 'year', y = 'pop', color='country',title='Population By Country').show()

    df_tips = px.data.tips()
    px.bar(df_tips, x='day',y='tip',color='sex',title='Tips by Sex on Each Day',
            labels={'tip': 'Tip Amount', 'day': 'Day of the Week'}).show()
    
    px.bar(df_tips, x='sex', y='total_bill', color='smoker', barmode='group').show()

    df_europe = px.data.gapminder().query("continent == ['Europe','Asia','Americas'] and year == 2007 and gdpPercap >= 35000")
    #print(df_europe)
    fig = px.bar(df_europe, y='gdpPercap', x='country', color='country', text='gdpPercap')
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8)
    fig.update_layout(xaxis_tickangle=-45)
    fig.show()


def animated_plots():
    df_cnt = px.data.gapminder()
    px.scatter(df_cnt, x="gdpPercap", y="lifeExp",
    animation_frame="year", 
    animation_group="country",
    size="pop", color='continent', hover_name='country',log_x=True,size_max=55, range_x=[100,100000],
    range_y=[25,90]).show()

if __name__ == "__main__":
    #demo1()
    #line_graph()
    #bar_chart()
    animated_plots()
