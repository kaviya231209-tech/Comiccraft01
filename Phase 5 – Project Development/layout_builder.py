def build_comic_layout(image_paths, full_story, outline):
    """Match each generated image with its corresponding panel text."""
    story_blocks = [b.strip() for b in full_story.split("\n\n") if b.strip()]

    layout = []
    for index, (image_path, panel_info) in enumerate(
        zip(image_paths, outline), start=1
    ):
        text = story_blocks[index - 1] if index - 1 < len(story_blocks) else (
            panel_info.get("scene_description", "")
        )
        layout.append({
            "panel": index,
            "title": panel_info.get("title", f"Panel {index}"),
            "image_path": image_path,
            "text": text,
            "scene_description": panel_info.get("scene_description", ""),
            "image_prompt": panel_info.get("image_prompt", "")
        })

    return layout
