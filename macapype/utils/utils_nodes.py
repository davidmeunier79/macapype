from nipype.pipeline.engine import Node
from nipype.interfaces.base import isdefined

class NodeParams(Node):

    """
    Overloading of the class nodes for aloowing params reading directly from
    a dictionnary; ultimately should be added to nipype if required
    """
    def __init__(
            self,
            interface,
            name,
            params={}):

        super(NodeParams, self).__init__(interface=interface, name=name)

        self.load_inputs_from_dict(params)

    def load_inputs_from_dict(self, params):

        new_inputs = list(set(list(params.keys())))
        for key in new_inputs:
            assert hasattr(self._interface.inputs, key), \
                print("Warning, Could not find {} in inputs {} for node {}".
                      format(key, self._interface.inputs, self._name))
            setattr(self._interface.inputs, key, params[key])


from nipype.interfaces.io import BIDSDataGrabber
from .misc import parse_key

class BIDSDataGrabberParams(BIDSDataGrabber):
    def __init__(self, params={}, **kwargs):

        super(BIDSDataGrabberParams, self).__init__(**kwargs)

        self._params = params

        print(self._params)

    def _set_indiv_params(self, outputs):

        assert "subject" in self._infields and "session" in self._infields, \
            "Error, subject and session should be defined as iterables"

        keys = ("sub-" + getattr(self.inputs, "subject"),
               "ses-" + getattr(self.inputs, "session"))

        outputs["indiv_params"] = parse_key(self._params, keys)

        return outputs

    def _list_outputs(self):

        outputs = super(BIDSDataGrabberParams, self)._list_outputs()

        outputs = self._set_indiv_params(outputs)

        return outputs


