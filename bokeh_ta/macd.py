from bokeh.models import ColumnDataSource, Legend
from bokeh.plotting import Figure, figure


def macd(source, fast, slow, signal, **figure_kwargs):  # API should match pandas_ta

    onesource = source

    # Note column name computation should match pandas_ta
    yfast = f"MACD_{fast}_{slow}_{signal}"
    yslow = f"MACDS_{fast}_{slow}_{signal}"
    y1hist = f"MACDH_{fast}_{slow}_{signal}"

    def render(**figure_kwargs):

        figure = Figure(**figure_kwargs)
        figure.add_layout(Legend())
        figure.legend.location = "top_left"
        figure.legend.click_policy = "hide"

        figure.line(legend_label=yfast,
                    source=onesource,
                    x='datetime',
                   y=yfast,
                   color='red')
        figure.line(legend_label=yslow,
                   source=onesource,
                    x='datetime',
                   y=yslow,
                   color='blue')
        figure.segment(legend_label=y1hist,
                      source=onesource,
                       x0='datetime', x1='datetime',
                      y0=0, y1=y1hist,
                      line_width=6, color='black',
                      alpha=0.5)

        return figure

    return render


if __name__ == '__main__':
    # A simple demo of outputting a figure to html file
    import pandas
    import pandas_ta
    dataframe = pandas.DataFrame.from_records(
        # TODO : sample data from csv / cassettes ?
        [[1581024000, "8885.6", "8885.6", "8870.0", "8870.1", "8882.6", "3.40642649", 23],
         [1581024060, "8870.1", "8871.3", "8863.5", "8870.3", "8869.1", "1.51573747", 21],
         [1581024120, "8871.3", "8872.8", "8867.8", "8869.9", "8871.5", "2.55702814", 16],
         [1581024180, "8869.9", "8880.1", "8869.9", "8880.1", "8876.9", "5.59530296", 21],
         [1581024240, "8877.9", "8880.5", "8877.9", "8880.1", "8880.2", "0.58048481", 11],
         [1581024300, "8880.1", "8880.1", "8878.8", "8879.3", "8879.1", "0.10505158", 4],
         [1581024360, "8879.3", "8880.0", "8879.0", "8879.0", "8879.0", "0.12800715", 3],
         [1581024420, "8879.4", "8883.2", "8879.4", "8882.9", "8881.8", "0.21217143", 8],
         [1581024480, "8883.1", "8883.1", "8879.5", "8882.5", "8882.2", "1.06838783", 31],
         [1581024540, "8881.1", "8882.5", "8879.3", "8882.4", "8881.3", "0.12026107", 10],
         [1581024600, "8882.4", "8882.4", "8875.3", "8875.3", "8881.5", "1.89192643", 17],
         [1581024660, "8875.2", "8875.2", "8869.0", "8873.2", "8869.9", "2.68435432", 18],
         [1581024720, "8873.2", "8874.0", "8871.7", "8872.8", "8872.8", "0.27668860", 13],
         ],
        columns=["timestamp", "open", "high", "low", "close", "vwap", "volume", "count"],
    )
    # minimum processing to be compatible with MACDFigure
    dataframe['datetime'] = pandas.to_datetime(dataframe.timestamp, unit="s")

    # TODO : this seems necessary now but shouldn't (check with pandas_ta)
    dataframe.close = pandas.to_numeric(dataframe.close)

    macddata = dataframe.ta.macd(fast=3, slow=6)
    macddata['datetime'] = dataframe.datetime

    source = ColumnDataSource(data=macddata, name="MACD")

    # Note arguments should match pandas_ta
    macdv = macd(source=source, fast=3, slow=6, signal=9)

    from bokeh.io import output_file
    from bokeh.plotting import save

    output_file(f"macd_sample.html", mode='inline')
    save(macdv(
        plot_height=240, tools='xpan, xwheel_zoom', toolbar_location="left",
        active_drag="xpan", active_scroll="xwheel_zoom",
        title="MACD",
        x_axis_type="datetime", y_axis_location="right",
        sizing_mode="scale_width",
    ))
