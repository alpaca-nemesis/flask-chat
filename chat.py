# -*- coding: UTF-8 -*-
import openai
import os
import sqlite3

# conn = sqlite3.connect(':memory:', check_same_thread=False)
conn = sqlite3.connect('test.db', check_same_thread=False)

c = conn.cursor()


def history_gpt(prompt, userID):
    try:
        cursor = c.execute('SELECT CONTENT FROM ' + userID)
    except sqlite3.OperationalError as e:
        # c.execute('CREATE TABLE ' + userID +'(ID INT PRIMARY KEY NOT NULL, CONTENT TEXT)')
        c.execute('CREATE TABLE ' + userID + ' (CONTENT TEXT)')
        conn.commit()
        print(e)

    if prompt == "重置":
        c.execute('DROP TABLE ' + userID)
        return ''
    else:
        sql = 'INSERT INTO ' + userID + ' (CONTENT) VALUES (\'' + prompt + '\')'
        print(sql)
        c.execute(sql)
        conn.commit()

    cursor = c.execute('SELECT CONTENT FROM ' + userID)
    hist = []
    for row in cursor:
        hist.append(row[0])
    input_text = "\n".join(hist)
    return input_text


# 获取环境变量的值并设置API密钥
openai.api_key = os.getenv("OPENAI_API_KEY")
# print(os.getenv("OPENAI_API_KEY"))
history = []


def chat_gpt2(prompt, userID):
    input_text = history_gpt(prompt, userID)
    if prompt == "重置":
        return "重置完成"
    # 调用 ChatGPT 接口
    model_engine = "text-davinci-003"
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=input_text,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    response = completion.choices[0].text.strip()
    return response


def chat_gpt(prompt, userID):
    global history

    if prompt == "重置":
        history = []
        return "重置完成"
    # 组合历史与输入问题
    input_text = "\n".join(history + [prompt])
    # 调用 ChatGPT 接口
    model_engine = "text-davinci-003"
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=input_text,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    response = completion.choices[0].text.strip()
    history.append(prompt)
    history.append(response)
    return response


if __name__ == "__main__":
    chat_gpt2('我叫陈世芳', 'admin1')
