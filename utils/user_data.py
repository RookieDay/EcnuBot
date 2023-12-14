import os
import time
import pandas as pd

file_name = "user_QA.csv"

async def storge_data(from_wxid, text_prompt, response, local_time):
    if not os.path.exists(file_name):
        with open(file_name, mode="w", encoding="utf-8") as f:
            local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            user_dict = {
                "from_wxid": from_wxid,
                "question": text_prompt,
                "response": response,
                "date_time": local_time,
            }
            data_header = pd.DataFrame(user_dict, index=[0])
            data_header.to_csv(file_name, index=False)

    else:
        user_QA = pd.read_csv(file_name)
        user_df = pd.DataFrame(
            [[from_wxid, text_prompt, response, local_time]],
            columns=["from_wxid", "question", "response", "date_time"],
            index=[len(user_QA)],
        )
        user_dfNew = pd.concat([user_QA, user_df], ignore_index=True)
        print(user_dfNew)
        user_dfNew.to_csv(file_name, index=False)