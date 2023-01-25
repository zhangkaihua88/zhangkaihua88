class ADDTable():
    def __init__(
        self,
        table_name,
        columns,
    ):
        self.base_user = "zhangkaihua88"
        self.table_name = table_name
        self.table_content = []
        self.columns = [item for item in columns if item.lower() in ["name", "language", "stars", "downloads", "version", "license", "other"]]

    def append(
        self,
        content,
        repo_name,
        name=None,
        language=None,
        stars=None,
        downloads=None,
        version=None,
        license=None,
        other=None,
    ):
        content = {
            'content': content,
            'repo_name': repo_name,
        }
        content["name"] = name if name else f"https://github.com/{self.base_user}/{repo_name}" 
        content["language"] = language if language else f"https://img.shields.io/github/languages/top/{self.base_user}/{repo_name}"
        content["stars"] = stars if stars else f"https://img.shields.io/github/stars/{self.base_user}/{repo_name}"
        content["downloads"] = downloads if downloads else f"https://img.shields.io/github/downloads/{self.base_user}/{repo_name}/total?color=success"
        content["version"] = version if version else f"https://img.shields.io/github/v/release/{self.base_user}/{repo_name}"
        content["license"] = license if license else f"https://img.shields.io/github/license/{self.base_user}/{repo_name}"
        content["other"] = other if other else ""
        self.table_content.append(content)
    def get_item_column(self, item, column):
        if column == "name":
            return f"**[{item['content']}]({item['name']})**"
        elif column == "language":
            return f"![]({item['language']})"
        elif column == "stars":
            return f"![]({item['stars']})"
        elif column == "downloads":
            return f"![]({item['downloads']})"
        elif column == "version":
            return f"![]({item['version']})"
        elif column == "license":
            return f"![]({item['license']})"
        elif column == "other":
            return f"{item['other']}"

    def generate_table(self):
        table = f"- **{self.table_name}**\n\n"
        table += f"  |{'|'.join([item.capitalize() for item in self.columns])}|\n"
        table += f"  |{'|'.join([':-:' for item in self.columns])}|\n"
        for item in self.table_content:
            table += f"  |{'|'.join([self.get_item_column(item, column) for column in self.columns])}|\n"
        table += "\n"
        return table

all_table = ""

ql_plugin_table = ADDTable("[QuickLook](https://github.com/QL-Win/QuickLook) Plugin", ["name", "language", "stars", "downloads", "version", "license"])
ql_plugin_table.append("JupyterNotebookViewer", "QuickLook.Plugin.JupyterNotebookViewer")
ql_plugin_table.append("XMindViewer-Thumbnail", "QuickLook.Plugin.XMindViewer-Thumbnail")
ql_plugin_table.append("KritaVirwer-MergedImage", "QuickLook.Plugin.KritaVirwer-MergedImage")
ql_plugin_table.append("CorelDrawViewer-Thumbnail", "QuickLook.Plugin.CorelDrawViewer-Thumbnail")
ql_plugin_table.append("DDSViewer", "QuickLook.Plugin.DDSViewer")
all_table += ql_plugin_table.generate_table()

competition_table = ADDTable("Competition Repo", ["name", "other", "language", "stars", "license"])
competition_table.append("2022人民网人工智能算法挑战赛-微博流行度预测", "2022WeiboPopularityPrediction", other="Rank 1")
all_table += competition_table.generate_table()

other_table = ADDTable("Other Repo", ["name", "language", "stars", "downloads", "version", "license"])
# other_table.append("ReadMe-Profile", "zhangkaihua88")
other_table.append("BUAA-Postgraduate-Aischedule", "BUAA-Postgraduate-Aischedule", downloads="https://www.zkhweb.top/VercelAPI/api/MIAISchedule/usage_badge.svg")
other_table.append("BUAA-Thesis-Download", "BUAA-Thesis-Download")
all_table += other_table.generate_table()

with open("init.md", "r", encoding="utf-8") as f:
    readme = f.read()
    readme = readme.replace("<!-- [**REPO**] -->", all_table)
with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme)