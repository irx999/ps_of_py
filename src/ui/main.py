import os

import streamlit as st
from streamlit import session_state as ss

from plugins.ps_of_py.src.ps_of_py import Image_utils, LoadData, Photoshop
from src.ui.utils import st_file_picker, st_folder_picker

if ss.get("ps_of_py_logs", []) is None:
    ss.ps_of_py_logs = []


def load_ps_settings():
    with st.expander("⚙️ PSD文件配置", expanded=True):
        # PSD文件配置
        c1 = st.columns([1, 1, 1.5])
        with c1[0]:
            psd_name_path = st_file_picker("选择PSD文件", button_icon="📄")
        with c1[1]:
            if st.button("获取psd信息", icon="📄"):
                with c1[2].spinner("处理中...", show_time=True):
                    try:
                        ps_settings = ss["ps_settings"]
                        ps = Photoshop(**ps_settings)
                        ss["psd_info"] = ps.get_psd_info()
                        st.toast("获取psd信息成功", icon="✅")
                    except Exception as e:
                        st.error(e)
        st.badge(str(psd_name_path), icon="📄")

    with st.expander("⚙️ 导出配置", expanded=True):
        c1 = st.columns([1, 1, 1.5])
        with c1[0]:
            export_folder = st_folder_picker("设置导出文件夹", button_icon="📁")

        with c1[1]:
            if st.button("打开导出文件夹", icon="📂"):
                os.startfile(str(export_folder))
        st.badge(str(export_folder), icon="📁")
        c2 = st.columns(3)
        file_format = c2[0].segmented_control(
            "导出格式", ["png", "jpg"], key="file_format", default="png"
        )
        close_ps = c2[1].segmented_control(
            "完成后关闭PSD", options=[True, False], key="close_ps", default=True
        )
        need_merge = c2[2].segmented_control(
            "同文件夹是否合并",
            options=[True, False],
            key="need_merge",
            default=True,
        )
        c3 = st.columns([1, 1, 1])
        suffix = c3[0].text_input("文件名后缀", "", key="suffix", icon="📄")
        need_merge_suffix = c3[1].text_input(
            "合并后缀", key="need_merge_suffix", value="(1)"
        )
        need_merge_width = c3[2].number_input(
            "合并宽度", key="need_merge_width", value=750, step=10
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
            "need_merge_width": need_merge_width if need_merge else 750,
        }

    ss["ps_settings"] = settings


def run_ps(ps_settings: dict, load_data):
    ps = Photoshop(**ps_settings)
    with st.spinner("执行PS任务中", show_time=True):
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
                ss["ps_of_py_logs"].append(
                    "保存成功: " + ps.export_folder + "/" + merge_list[0] + ps.suffix
                )

            # ps.app.doJavaScript(f'alert("save to jpg: {ps.export_folder}")')
        st.toast("PS任务执行完成", icon="✅")
    if ps_settings["need_merge"]:
        with st.spinner("执行合并任务中", show_time=True):
            for merge_name, merge_list in merge_dict.items():
                try:
                    Image_utils.merge_images(
                        ps.export_folder + "/" + merge_name,
                        merge_list,
                        merge_name
                        + ps_settings["need_merge_suffix"]
                        + "."
                        + ps_settings["file_format"],
                        width=ps_settings["need_merge_width"],
                    )
                    ss["ps_of_py_logs"].append(
                        "合并成功: "
                        + ps.export_folder
                        + "/"
                        + merge_name
                        + ps_settings["need_merge_suffix"]
                    )
                except Exception as e:
                    st.error(e)

        st.toast("合并任务执行完成", icon="✅")


def show():
    st.set_page_config(page_title="🎨ps_of_py自动化工具", layout="wide")

    header = st.columns([3, 1, 1], vertical_alignment="bottom")
    header[0].header("🎨ps_of_py自动化工具")

    ps_settings = ss.get("ps_settings", load_ps_settings())

    if header[1].button("一键启动", icon="🚀"):
        with st.spinner("处理中...", show_time=True):
            try:
                run_ps(ps_settings, load_data=LoadData())
            except FileNotFoundError as e:
                st.toast(e, icon="❌")
            except Exception as e:
                st.toast(e, icon="❌")

    @st.dialog("ps_of_py_logs 查看", icon="📝")
    def 日志():
        for i in ss.get("ps_of_py_logs", []):
            st.text(i)

    if header[2].button("查看日志", icon="📝"):
        日志()
    # 主界面
    tab1, tab2, tab3 = st.tabs(["📊 Excel表格加载", "🎨 psd信息加载", "🖼️ None"])

    with tab1:
        pass

    with tab2:
        st.write(ss.get("psd_info", {}))

    with tab3:
        pass


if __name__ == "__main__":
    show()
