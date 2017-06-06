from pyexcel.internal.common import ChartPluginChain


ChartPluginChain(__name__).add_a_plugin(
    submodule='plot.SimpleLayout',
    tags=['xy']
)
