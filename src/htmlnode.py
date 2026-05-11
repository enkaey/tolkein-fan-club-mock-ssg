class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if self.props is None:
            return ''
        to_return = "".join([f' {attr}="{value}"' for attr, value in self.props.items()])

        return to_return

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag!r}, {self.value!r}, children: {self.children!r}, {self.props!r})"