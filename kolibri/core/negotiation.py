from rest_framework.negotiation import DefaultContentNegotiation
from rest_framework.renderers import JSONRenderer


class LimitContentNegotiation(DefaultContentNegotiation):
    def select_renderer(self, request, renderers, format_suffix=None):
        """
        Always return JSONRenderer unless for morango
        """
        if request.path.startswith("/api/morango"):
            return super(LimitContentNegotiation, self).select_renderer(
                request, renderers, format_suffix=None
            )
        renderer = JSONRenderer()
        return (renderer, renderer.media_type)
