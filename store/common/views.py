class TitleMixin:
    title = None

    def get_context_data(self, **kwargs):
        """
        The get_context_data function is a method of the TemplateView class.
        It takes in **kwargs, which are keyword arguments that can be passed to the function
        The super() function returns an object representing the parent class of TitleMixin,
        which is TemplateView. The get_context_data method from this parent class is called with
        the same keyword arguments as were passed to get_context_data in TitleMixin (**kwargs).
        This means that all context data returned by TemplateView's get_context data will also be available in our view.
        """
        context = super(TitleMixin, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context
