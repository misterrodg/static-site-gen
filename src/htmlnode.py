class HTMLNode:
    def __init__(self, tag = None, value = None, children = [], props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        tag = self.tag if self.tag else ""
        value = self.value if self.value else ""
        children = ""
        if self.children:
            children += f" with {len(self.children)} children"
        props = ""
        if self.props:
            props += " with props "
            props += self.props_to_html()

        return f"{tag} {value}{children}{props}"

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        result = []
        if self.props:
            for k, v in self.props.items():
                result.append(f"{k}=\"{v}\"")
            return " " + " ".join(result)
        return ""

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag=tag,value=value,props=props)
        self.tag = tag
        self.value = value
        self.props = props

    def to_html(self):
        if not self.value:
            raise ValueError("All leaf nodes must have a value.")
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

