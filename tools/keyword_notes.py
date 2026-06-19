from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

# 示例配置数据
SAMPLE_PORTAL_URL = "https://webportal-hth.com.cn"
SAMPLE_KEYWORD = "华体会"


@dataclass
class KeywordNote:
    """关键词笔记的数据类"""
    keyword: str
    note: str
    url: str
    created_at: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)
    priority: int = 1  # 1-5, 5 最高

    def to_formatted_string(self, include_metadata: bool = True) -> str:
        """格式化输出单条笔记"""
        lines = [
            f"关键词: {self.keyword}",
            f"笔记: {self.note}",
            f"来源: {self.url}",
        ]
        if include_metadata:
            lines.append(f"创建时间: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            lines.append(f"优先级: {self.priority}")
            if self.tags:
                lines.append(f"标签: {', '.join(self.tags)}")
        return "\n".join(lines)

    def to_short_summary(self) -> str:
        """简短摘要"""
        return f"[{self.keyword}] {self.note[:30]}... ({self.url})"


@dataclass
class KeywordNoteCollection:
    """关键词笔记集合"""
    notes: List[KeywordNote] = field(default_factory=list)

    def add_note(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def add_sample_data(self) -> None:
        """添加一些示例笔记数据"""
        self.notes.append(
            KeywordNote(
                keyword=SAMPLE_KEYWORD,
                note="这是一个示例笔记，用于演示如何组织关键词信息。",
                url=SAMPLE_PORTAL_URL,
                tags=["示例", "演示"],
                priority=3,
            )
        )
        self.notes.append(
            KeywordNote(
                keyword=SAMPLE_KEYWORD,
                note="第二个示例笔记，展示不同的内容结构。",
                url=SAMPLE_PORTAL_URL + "/page2",
                tags=["示例", "测试"],
                priority=2,
            )
        )

    def find_by_keyword(self, keyword: str) -> List[KeywordNote]:
        """按关键词查找笔记"""
        return [note for note in self.notes if note.keyword == keyword]

    def find_by_tag(self, tag: str) -> List[KeywordNote]:
        """按标签查找笔记"""
        return [note for note in self.notes if tag in note.tags]

    def sort_by_priority(self, descending: bool = True) -> None:
        """按优先级排序"""
        self.notes.sort(key=lambda n: n.priority, reverse=descending)

    def format_all(self, include_metadata: bool = True) -> str:
        """格式化输出所有笔记"""
        if not self.notes:
            return "暂无笔记内容。"
        parts = [f"关键词笔记集合（共 {len(self.notes)} 条）", "=" * 40]
        for i, note in enumerate(self.notes, 1):
            parts.append(f"\n--- 笔记 {i} ---")
            parts.append(note.to_formatted_string(include_metadata))
        return "\n".join(parts)

    def export_as_text(self, filepath: str = "notes_export.txt") -> None:
        """导出笔记到文本文件"""
        content = self.format_all()
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"笔记已导出到: {filepath}")


def demo_usage() -> None:
    """演示函数：展示 KeywordNote 和 KeywordNoteCollection 的基本用法"""
    print("=== 关键词笔记演示 ===\n")

    # 创建集合并添加示例数据
    collection = KeywordNoteCollection()
    collection.add_sample_data()

    # 手动添加一条笔记
    extra_note = KeywordNote(
        keyword="华体会",
        note="通过配置文件直接创建的新笔记。",
        url="https://webportal-hth.com.cn/notes",
        tags=["手动", "配置"],
        priority=4,
    )
    collection.add_note(extra_note)

    # 输出所有笔记
    print(collection.format_all(include_metadata=True))

    # 演示查找功能
    print("\n=== 按标签查找 ===")
    for note in collection.find_by_tag("示例"):
        print(note.to_short_summary())

    print("\n=== 按优先级排序后的第一条 ===")
    collection.sort_by_priority()
    print(collection.notes[0].to_formatted_string())


if __name__ == "__main__":
    demo_usage()