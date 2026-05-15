from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[object], props=None):
        if children is not None:
            if not isinstance(children, list):
                raise TypeError("Children must be a list of HTMLNode objects")
            
            for child in children:
                if not isinstance(child, HTMLNode):
                    raise TypeError(f"All children must be HTMLNode instances, got {type(child)}")
            
        super().__init__(tag, None, children, props)
    
    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("Invalid HTML: no tag")
        if not self.children:
            raise ValueError("Invalid HTML: no children")
        
        children_html = "".join([child.to_html() for child in self.children])
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"