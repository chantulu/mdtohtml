class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplemented()
    
    def props_to_html(self) -> str:
        prop = ""
        if self.props is not None:
            for key in self.props:
                prop += f"{key}=\"{self.props[key]}\" "
            prop = " " + prop.rstrip()
        return prop
    
    def __repr__(self):
        childrn = {}
        if self.children is not None and len(self.children) > 0:
            for child in self.children:
                if child.tag not in childrn:
                    childrn[child.tag] = 1
                else:
                    childrn[child.tag] += 1
        return f"tag:{self.tag}\nvalue:{self.value}\nchildren:{childrn}\nprops:{self.props_to_html()}"

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None) -> None:
        if value is None:
            raise ValueError("value is required")
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None) -> None:
        if children is None:
            raise ValueError("value is required")
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid HTML: no tag")
        ret = ""
        if self.children is None:
            return ret + self.to_html()
        else:
            for c in self.children:
                ret += c.to_html()
        return f"<{self.tag}{self.props_to_html()}>{ret}</{self.tag}>"
        