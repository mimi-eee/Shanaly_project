import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import panel as pn
import requests
from dotenv import load_dotenv
from pathlib import Path
import os
from time import sleep
from datetime import datetime

# Dot Env File
dotenv_path = Path('./.env')
load_dotenv(dotenv_path=dotenv_path)

# Environment Variables
BASE_URL = os.environ.get("BASE_URL_PANEL")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD_PANEL")

# Python Panel Code Starts
pn.config.theme = 'default'

btn_criminal_stat = pn.widgets.Button(name="ユーザー報告集計", button_type="primary", styles={"width": "100%"})
btn_read_post_reply = pn.widgets.Button(name="投稿/返信の確認", button_type="primary", styles={"width": "100%"})
btn_criminal_action = pn.widgets.Button(name="ユーザー対応", button_type="primary", styles={"width": "100%"})
btn_recommend_post = pn.widgets.Button(name="投稿おすすめ", button_type="primary", styles={"width": "100%"})
btn_delete_post_reply = pn.widgets.Button(name="投稿/返信の削除", button_type="danger", styles={"width": "100%"})
btb_delete_criminal_post_reply = pn.widgets.Button(name="ユーザーの投稿/返信の削除", button_type="danger", styles={"width": "100%"})
btn_update_wiki = pn.widgets.Button(name="用語検索管理", button_type="primary", styles={"width": "100%"})
btn_stat_num_users = pn.widgets.Button(name="ユーザー統計", button_type="primary", styles={"width": "100%"})

def show_app(app_key):
    main_area.clear()
    main_area.append(mapping[app_key])

btn_criminal_stat.on_click(lambda event: show_app("btn_criminal_stat"))
btn_read_post_reply.on_click(lambda event: show_app("btn_read_post_reply"))
btn_criminal_action.on_click(lambda event: show_app("btn_criminal_action"))
btn_recommend_post.on_click(lambda event: show_app("btn_recommend_post"))
btn_delete_post_reply.on_click(lambda event: show_app("btn_delete_post_reply"))
btb_delete_criminal_post_reply.on_click(lambda event: show_app("btb_delete_criminal_post_reply"))
btn_update_wiki.on_click(lambda event: show_app("btn_update_wiki"))
btn_stat_num_users.on_click(lambda event: show_app("btn_stat_num_users"))

# Criminals Statistics
def CriminalStat():

    # pn.bind() + no output at first + manual update + not continous + loading spinner effect
    button = pn.widgets.Button(name="更新", width=200, height=50)

    def get_data(click):
        if click:
            with pn.param.set_values(app, loading=True): # loading effect
                sleep(1) # this is for simulating loading spinner effect

                # Get data
                res = requests.get(f'{BASE_URL}/api/admin/list/potential_criminals')

                if res.status_code == 200:
                    
                    data = res.json()

                    df_stat = (
                        pd
                        .DataFrame
                        .from_dict(data["criminal_stat"])
                        .rename(columns={"criminal_id":"id"})
                    )
                    df_info = (
                        pd
                        .DataFrame
                        .from_dict(data["criminal_info"])
                    )

                    return (
                        df_stat
                        .merge(
                            df_info,
                            how="inner",
                            on="id"
                        )
                        .loc[:,["id","username","num_reported","is_blocked"]]
                        .rename(columns={
                            "id": "ユーザーID",
                            "username": "ユーザー名",
                            "num_reported": "申告された数",
                            "is_blocked": "ブロック状態",
                        })
                        .set_index("ユーザーID")
                    )
                else:
                    return res.json()["detail"]

    bind_func = pn.bind(
        get_data,
        button
    )

    app = pn.Column(
        "# ユーザー申告集計",
        button,
        bind_func
    )
    return app

# Criminal's Posts/Replies
def ReadPostReply():

    # pn.bind() + no output at first + manual update + not continous + loading spinner effect
    select = pn.widgets.Select(name='選択', options=["-",'投稿', '返信'], value="-")
    user_id_input = pn.widgets.TextInput(name='ユーザーID', placeholder='User ID...')
    button = pn.widgets.Button(name="実行", width=200, height=50)

    def get_data(click):
        if click:
            with pn.param.set_values(app, loading=True): # loading effect
                
                sleep(1) # this is for simulating loading spinner effect

                option = select.value
                user_id = user_id_input.value

                if option == "-":
                    return "何を確認するかを指定してください。"
                if user_id == "" or user_id == None:
                    return "ユーザーIDを入力してください。"
                
                params = {'user_id': int(user_id)}

                if option == "投稿":
                    endpoint = f'{BASE_URL}/api/admin/list/criminal_post'
                if option == "返信":
                    endpoint = f'{BASE_URL}/api/admin/list/criminal_reply'

                # Get data
                res = requests.get(endpoint, params=params)

                if res.status_code == 200:
                    
                    data = res.json()

                    if option == "投稿":

                        df = (
                            pd
                            .DataFrame
                            .from_dict(data)
                            .assign(content=lambda df_: df_["content"].str.replace(r'<[^<>]*>', '', regex=True))
                            .rename(columns={
                                "id": "投稿ID",
                                "title": "タイトル",
                                "content": "コンテンツ",
                                "tags": "タグ",
                                "created_at": "作成時刻",
                                "modified_at": "修正時刻",
                                "user_id": "ユーザーID",
                            })
                            .set_index("投稿ID")
                        )
                    
                    if option == "返信":

                        df = (
                        pd
                        .DataFrame
                        .from_dict(data)
                        .rename(columns={
                            "id": "返信ID",
                            "content": "返信内容",
                            "created_at": "作成時刻",
                            "user_id": "ユーザーID",
                        })
                        .set_index("返信ID")
                    )
                    
                    return df

                else:
                    return res.json()["detail"]

    bind_func = pn.bind(
        get_data,
        button
    )

    app = pn.Column(
        "# ユーザーの投稿/返信の確認",
        select,
        user_id_input,
        button,
        bind_func,
    )
    return app

# Actions for Criminal
def CriminalAction():

    # pn.bind() + no output at first + manual update + not continous + loading spinner effect
    select = pn.widgets.Select(name='選択', options=["-",'ブロック', 'アンブロック',"報告リセット"], value="-")
    user_id_input = pn.widgets.TextInput(name='ユーザーID', placeholder='User ID...')
    button = pn.widgets.Button(name="実行", width=200, height=50)

    def get_data(click):
        if click:
            with pn.param.set_values(app, loading=True): # loading effect
                
                sleep(1) # this is for simulating loading spinner effect

                option = select.value
                user_id = user_id_input.value

                if option == "-":
                    return "ユーザーに対してどのような処理をするかを指定してください。"
                if user_id == "" or user_id == None:
                    return "ユーザーIDを入力してください。"
                
                body = {"criminal_id": int(user_id), "password": ADMIN_PASSWORD}

                if option == "ブロック":
                    endpoint = f'{BASE_URL}/api/admin/block'
                if option == "アンブロック":
                    endpoint = f'{BASE_URL}/api/admin/unblock'
                if option == "報告リセット":
                    endpoint = f'{BASE_URL}/api/admin/reset'

                # Get data
                res = requests.patch(endpoint, json=body)

                if res.status_code == 200:
                    
                    data = res.json()
                    if option == "ブロック":
                        return f"[Block] ユーザーID = {data['id']}, ユーザー名 = {data['username']}, ブロック状態 = {data['is_blocked']}"
                    if option == "アンブロック":
                        return f"[Unblock] ユーザーID = {data['id']}, ユーザー名 = {data['username']}, ブロック状態 = {data['is_blocked']}"
                    if option == "報告リセット":
                        return res.json()["detail"]
                else:
                    return res.json()["detail"]

    bind_func = pn.bind(
        get_data,
        button
    )

    app = pn.Column(
        "# ユーザー対応",
        select,
        user_id_input,
        button,
        bind_func,
    )
    return app

# Recommend a Post
def RecommendPost():

    # pn.bind() + no output at first + manual update + not continous + loading spinner effect
    post_id_input = pn.widgets.TextInput(name='投稿ID', placeholder='Post ID...')
    button = pn.widgets.Button(name="実行", width=200, height=50)

    def get_data(click):
        if click:
            with pn.param.set_values(app, loading=True): # loading effect
                
                sleep(1) # this is for simulating loading spinner effect

                post_id = post_id_input.value
                if post_id == "" or post_id == None:
                    return "投稿IDを入力してください。"
                
                body = {"post_id": int(post_id), "password": ADMIN_PASSWORD}

                # Get data
                res = requests.post(f'{BASE_URL}/api/admin/recommend', json=body)

                if res.status_code == 200:
                    return res.json()["detail"]
                else:
                    return res.json()["detail"]

    bind_func = pn.bind(
        get_data,
        button
    )

    app = pn.Column(
        "# 投稿おすすめ",
        post_id_input,
        button,
        bind_func,
    )
    return app

# Remove Criminal's Post or Reply
def DeletePostReply():
    select = pn.widgets.Select(name='選択', options=["-",'投稿', '返信'], value="-")
    id_input = pn.widgets.TextInput(name='ID', placeholder='ID Number...')
    button = pn.widgets.Button(name="削除", width=200, height=50, button_type='danger')
    
    def get_data(click):
        if click:
            with pn.param.set_values(app, loading=True): # loading effect
                
                sleep(1) # this is for simulating loading spinner effect

                option = select.value
                target_id = id_input.value
                
                if option == "-":
                    return "何を削除するかを指定してください。"
                if target_id == "" or target_id == None:
                    return "IDを入力してください。"
                try:
                    int(target_id)
                except:
                    return "IDは文字はできません。"
                
                if option == "投稿":
                    endpoint = f'{BASE_URL}/api/admin/post'
                    body = {"post_id": int(target_id), "password": ADMIN_PASSWORD}
                if option == "返信":
                    endpoint = f'{BASE_URL}/api/admin/reply'
                    body = {"reply_id": int(target_id), "password": ADMIN_PASSWORD}
                
                # Delete data
                res = requests.delete(endpoint, json=body)
                if res.status_code == 200:
                    select.value = "-"
                    id_input.value = ""
                    return res.json()["detail"] + f"[{option}] ID = {target_id}"
                else:
                    return res.json()["detail"]

    bind_func = pn.bind(
        get_data,
        button
    )
    
    
    app = pn.Column(
        "# ユーザーの投稿/返信の削除",
        select,
        id_input,
        button,
        bind_func,
    )
    return app

# Remove a Criminal's All Posts or Replies
def DeleteCriminalPostReply():
    select = pn.widgets.Select(name='選択', options=["-",'投稿', '返信'], value="-")
    id_input = pn.widgets.TextInput(name='ユーザーID', placeholder='ID Number...')
    button = pn.widgets.Button(name="削除", width=200, height=50, button_type='danger')
    
    def get_data(click):
        if click:
            with pn.param.set_values(app, loading=True): # loading effect
                
                sleep(1) # this is for simulating loading spinner effect

                option = select.value
                target_id = id_input.value
                
                if option == "-":
                    return "何を削除するかを指定してください。"
                if target_id == "" or target_id == None:
                    return "IDを入力してください。"
                try:
                    int(target_id)
                except:
                    return "IDは文字はできません。"
                
                if option == "投稿":
                    endpoint = f'{BASE_URL}/api/admin/user_posts'
                    body = {"criminal_id": int(target_id), "password": ADMIN_PASSWORD}
                if option == "返信":
                    endpoint = f'{BASE_URL}/api/admin/user_replies'
                    body = {"criminal_id": int(target_id), "password": ADMIN_PASSWORD}
                
                # Delete data
                res = requests.delete(endpoint, json=body)
                if res.status_code == 200:
                    select.value = "-"
                    id_input.value = ""
                    return res.json()["detail"] + f"[{option}の削除完了] ユーザーID = {target_id}"
                else:
                    return res.json()["detail"]

    bind_func = pn.bind(
        get_data,
        button
    )
    
    app = pn.Column(
        "# ユーザーの全ての投稿/返信の削除",
        select,
        id_input,
        button,
        bind_func,
    )
    return app

# Update Wiki
def UpdateWiki():
    search_input = pn.widgets.TextInput(name='用語名')
    btn_search = pn.widgets.Button(name="検索", width=200, height=50)
    btn_clear = pn.widgets.Button(name="クリア", width=200, height=50)
    btn_update = pn.widgets.Button(name="変更", width=200, height=50, visible=False)

    id_input = pn.widgets.IntInput(name='ID', disabled=True, width=100)
    word_input = pn.widgets.TextAreaInput(name='word', auto_grow=True)
    category_input = pn.widgets.TextAreaInput(name='category', auto_grow=True)
    yomikata_input = pn.widgets.TextAreaInput(name='yomikata', auto_grow=True)
    description_input = pn.widgets.TextAreaInput(name='description (Markdown可能)', auto_grow=True, width=1000, height=150)
    link_input = pn.widgets.TextAreaInput(name='link', auto_grow=True, width=1000, disabled=True)
    ready_input = pn.widgets.Select(name='Ready', options=[True, False, None], value=None)
    
    
    def get_data(click):
        if click:
            with pn.param.set_values(app, loading=True): # loading effect
                
                sleep(1) # this is for simulating loading spinner effect

                if search_input.value == None or search_input.value.strip() == "":
                    return "## 用語を入力してください。"

                res = requests.get(f'{BASE_URL}/api/admin/wiki_get', params={"word": search_input.value})

                if res.status_code == 200:
                    id_input.value = res.json()["id"]
                    word_input.value = res.json()["word"]
                    yomikata_input.value = res.json()["yomikata"]
                    category_input.value = res.json()["category"]
                    description_input.value = res.json()["description"]
                    link_input.value = res.json()["link"]
                    ready_input.value = res.json()["ready"]

                    btn_update.visible = True
                else:
                    return res.json()["detail"]
                
    def clear(click):
        if click:
            search_input.value = ""
            id_input.value = 0
            word_input.value = ""
            category_input.value = ""
            yomikata_input.value = ""
            description_input.value = ""
            link_input.value = ""
            ready_input.value = None

            btn_update.visible = False

    def update_word(click):
        if click:
            with pn.param.set_values(app, loading=True): # loading effect
                sleep(1) # this is for simulating loading spinner effect

                if ready_input.value is None:
                    return "## ReadyはTrueかFalseしかできません。"

                body = {
                    "id": id_input.value,
                    "yomikata": yomikata_input.value ,
                    "category": category_input.value,
                    "description": description_input.value,
                    "link": link_input.value,
                    "ready": ready_input.value,

                    "password": ADMIN_PASSWORD,
                }

                res = requests.patch(f'{BASE_URL}/api/admin/wiki_modify', json=body)

                if res.status_code == 200:

                    id_input.value = 0
                    word_input.value = ""
                    category_input.value = ""
                    yomikata_input.value = ""
                    description_input.value = ""
                    link_input.value = ""
                    ready_input.value = None
                    btn_update.visible = False
                    
                    return "## " + res.json()["detail"]
                else:
                    return "## " + res.json()["detail"]

    search_bind_fn = pn.bind(
        get_data,
        btn_search,
    )

    clear_bind_fn = pn.bind(
        clear,
        btn_clear
    )

    update_bind_fn = pn.bind(
        update_word,
        btn_update
    )
    
    app = pn.Column(
        "# 用語のアップデート",
        search_input,
        pn.Row(btn_search, btn_clear),
        
        search_bind_fn,
        update_bind_fn,

        pn.Row(id_input, word_input, category_input, yomikata_input),
        description_input,
        link_input,
        ready_input,
        btn_update,

        clear_bind_fn,

    )
    return app

# User Statistics
def UserStat():

    # pn.bind() + no output at first + manual update + not continous + loading spinner effect
    button = pn.widgets.Button(name="更新", width=200, height=50)

    def get_data(click):
        if click:
            with pn.param.set_values(app, loading=True): # loading effect
                sleep(1) # this is for simulating loading spinner effect

                # Get data
                res = requests.get(f'{BASE_URL}/api/admin/stat/num_users_daily')

                if res.status_code == 200:
                    
                    data = res.json()

                    df = (
                        pd
                        .DataFrame
                        .from_records(data)
                        .rename(columns={"date":"日付","num_users":"ユーザー数"})
                        .set_index("日付")
                    )

                    fig, ax = plt.subplots(figsize=(4,3))
                    ax.bar(df.index, df["ユーザー数"])
                    ax.set_title("Daily Number of Users")

                    return pn.Column(
                        f"現時刻 = {datetime.now()}",
                        pn.Row(
                            df,
                            fig,
                        )
                    )
                else:
                    return res.json()["detail"]

    bind_func = pn.bind(
        get_data,
        button
    )

    app = pn.Column(
        "# ユーザー統計",
        button,
        bind_func
    )
    return app

mapping = {
    "btn_criminal_stat": CriminalStat(),
    "btn_read_post_reply": ReadPostReply(),
    "btn_criminal_action": CriminalAction(),
    "btn_recommend_post": RecommendPost(),
    "btn_delete_post_reply": DeletePostReply(),
    "btb_delete_criminal_post_reply": DeleteCriminalPostReply(),
    "btn_update_wiki": UpdateWiki(),
    "btn_stat_num_users": UserStat()
}

sidebar = pn.Column(
    btn_stat_num_users,
    btn_criminal_stat,
    btn_read_post_reply,
    btn_criminal_action,
    btn_recommend_post,
    btn_update_wiki,
    btn_delete_post_reply,
    btb_delete_criminal_post_reply,

	styles={"width": "100%", "padding": "10px"}
)

main_area = pn.Column(mapping["btn_stat_num_users"], styles={"width":"100%"})

template = pn.template.MaterialTemplate(
    title="Shanaly Admin App",
    sidebar=[sidebar],
    main=[main_area],
    sidebar_width=300,
)

template.servable()