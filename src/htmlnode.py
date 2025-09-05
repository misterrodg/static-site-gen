class HTMLNode:
    def __init__(
            self,
            tag: str | None = None,
            value: str | None = None,
            children: list = [],
            props: dict | None = None
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        tag = f"<{self.tag}>" if self.tag else None
        value = self.value if self.value else None
        children = ""
        if self.children:
            children += f" with {len(self.children)} children"
        props = ""
        if self.props:
            props += " with props "
            props += self.props_to_html()

        return f"{self.__class__.__name__}({tag}, {value}, {children}, {props})"

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
    def __init__(
        self,
        tag: str | None,
        value: str,
        props: dict | None = None,
        self_close: bool = False
    ):
        super().__init__(tag=tag,value=value,props=props)
        self.self_close = self_close

    def to_html(self):
        if self.value is None and not self.self_close:
            raise ValueError("Leaf nodes that aren't self-closing must have a value.")
        lead_tag = ""
        trail_tag = ""
        if self.tag:
            lead_tag = f"<{self.tag}{self.props_to_html()}>"
            trail_tag = f"</{self.tag}>"
        if self.self_close:
            lead_tag = lead_tag.replace(">","/>")
            trail_tag = ""
        return f"{lead_tag}{self.value}{trail_tag}"

class ParentNode(HTMLNode):
    def __init__(
            self,
            tag: str,
            children: list,
            props: dict | None = None
    ):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("All parent nodes must have a tag.")
        if not self.children:
            raise ValueError("All parent nodes must have one or more children.")
        child_string = ""
        for child in self.children:
            child_string += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{child_string}</{self.tag}>"

