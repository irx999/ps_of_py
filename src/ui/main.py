import os

import streamlit as st

from plugins.ps_of_py.src.ps_of_py import Image_utils, LoadData, Photoshop
from src.ui.utils import st_file_picker, st_folder_picker


def load_ps_settings():
    with st.expander("⚙️ 配置参数", expanded=True):
        # PSD文件配置
        psd_name_path = st_file_picker("选择PSD文件", button_icon="📄")
        st.badge(str(psd_name_path), icon="📁")
        c1 = st.columns([1, 1, 1])
        with c1[0]:
            export_folder = st_folder_picker("设置导出文件夹", button_icon="⚙️")

        with c1[1]:
            if st.button("打开导出文件夹", icon="📂"):
                os.startfile(str(export_folder))
        st.badge(str(export_folder), icon="📁")
        # 导出配置
        c2 = st.columns(4)
        suffix = c2[0].text_input("文件名后缀", "", key="suffix", icon="📄")
        file_format = c2[1].segmented_control(
            "导出格式", ["png", "jpg"], key="file_format", default="png"
        )
        close_ps = c2[2].segmented_control(
            "完成后关闭PSD", options=[True, False], key="close_ps", default=True
        )
        need_merge = c2[3].segmented_control(
            "是否合并", options=[True, False], key="need_merge", default=True
        )
        if need_merge:
            need_merge_suffix = c2[3].text_input(
                "合并后缀", key="need_merge_suffix", value="(1)"
            )
        settings: dict = {
            "psd_name": psd_name_path.name,
            "psd_dir_path": psd_name_path.parent._str,
            "export_folder": export_folder._str,
            "file_format": file_format if file_format else "png",
            "suffix": suffix,
            "colse_ps": close_ps if close_ps else False,
            "need_merge": need_merge if need_merge else False,
            "need_merge_suffix": need_merge_suffix if need_merge else "",
        }
    return settings


def show():
    st.set_page_config(page_title="Photoshop自动化工具", layout="wide")
    st.title("📸 Photoshop自动化工具")

    # 主界面
    tab1, tab2, tab3 = st.tabs(["📊 Excel表格加载", "🎨 None", "🖼️ None"])

    with tab1:
        st.header("配置设置")
        ps_settings = load_ps_settings()
        # st.write(ps_settings)
        # if st.button("获取psd信息"):
        #     with st.spinner("处理中..."):
        #         ps = Photoshop(**ps_settings)
        #         # st.write(ps.get_psd_info())

        if st.button("一键启动"):
            expander = st.expander("处理中...", expanded=True)
            with expander:
                ps = Photoshop(**ps_settings)
                load_data = LoadData()
                with ps:
                    # for merge_name in load_data.merge_names:

                    merge_dict = {}
                    for task in load_data.selected_skus():
                        merge_list = task["任务名"].split("|")
                        if len(merge_list) > 1:
                            if merge_list[0] not in merge_dict:
                                merge_dict[merge_list[0]] = []
                            merge_dict[merge_list[0]].append(
                                merge_list[1] + ps.suffix + "." + ps.file_format
                            )

                        ps.core(task["任务名"], task["修改信息"])
                        st.info(
                            "保存成功: "
                            + ps.export_folder
                            + "/"
                            + merge_list[0]
                            + ps.suffix
                        )

                    # ps.app.doJavaScript(f'alert("save to jpg: {ps.export_folder}")')

                if ps_settings["need_merge"]:
                    for merge_name, merge_list in merge_dict.items():
                        try:
                            Image_utils.merge_images(
                                ps.export_folder + "/" + merge_name,
                                merge_list,
                                merge_name
                                + ps_settings["need_merge_suffix"]
                                + "."
                                + ps_settings["file_format"],
                            )
                            st.info(
                                "合并成功: "
                                + ps.export_folder
                                + "/"
                                + merge_name
                                + ps_settings["need_merge_suffix"]
                            )
                        except Exception as e:
                            st.error(e)

                st.success("处理完成")

    with tab2:
        pass

    with tab3:
        pass


if __name__ == "__main__":
    show()
