from pyexcel_chart.plugin import ChartPluginChain


ChartPluginChain(__name__).add_a_plugin(
    submodule='plot.SimpleLayout',
    tags=['xy']
)
