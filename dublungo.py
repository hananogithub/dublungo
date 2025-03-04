import openai
from sentence_transformers import SentenceTransformer, util

def translate_chunk(chunk, target_language):
    """
    与えられたテキストチャンクを指定した言語に翻訳する関数。
    """
    messages = [
        {"role": "system", "content": "あなたは有能な翻訳アシスタントです。"},
        {"role": "user", "content": f"以下の文章を{target_language}に翻訳してください。\n\n{chunk}"}
    ]
    
    try:
        client = openai.OpenAI(api_key="") 
        response = client.chat.completions.create(
            model="gpt-4",  # 必要に応じて他のモデルに変更
            messages=messages,
            temperature=0.3,       # 低めの温度で安定した翻訳を期待
            max_tokens=2048        # チャンクサイズに合わせて調整
        )
        translated_text = response.choices[0].message.content.strip()
        return translated_text
    except Exception as e:
        print("翻訳中にエラーが発生しました:", e)
        return chunk  # エラー時は元のテキストを返す

def translate_file(traslation, translated_traslation, target_language):
    """
    テキストファイル全体を読み込み、チャンクごとに翻訳して結果を出力する関数。
    """
    lang_pair = list()
    # 入力ファイルの読み込み
    with open(translation, "r", encoding="utf-8") as f:
        for line in f:
            translated = translate_chunk(line, target_language)
            lang_pair.append((line,translated))
    f.close()

    return lang_pair

def read_file_by_newline(file_path):
    """
    指定したファイルを読み込み、改行ごとにリストの要素として格納する。
    """
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.read().splitlines()  # 改行を考慮して分割

    return lines

def find_max_similarity_pairs(similarity_pairs):
    """
    similarity_pairs の各 i に対して、3番目の要素 (cosine_score) が最大のリストを返す。

    Parameters:
    similarity_pairs (list of list): [[id1, id2, score], ...]

    Returns:
    list: 最大のスコアを持つリスト
    """
    max_pair = max(similarity_pairs, key=lambda x: x[2])  # 3番目の要素 (スコア) で最大を取得
    return max_pair

if __name__ == "__main__":
    original = "lesmiserables_fr.txt"
    translation = "lesmiserables_en.txt"          # 入力ファイル名（翻訳版テキスト）
    translation_in_target_language = "translation_in_target_laguage.txt"    # 出力ファイル名（原文への翻訳結果）
    target_language = "フランス語"                      # 例としてフランス語に翻訳（必要に応じて変更）
    
    trans_in_target = translate_file(translation, translation_in_target_language, target_language)
    print("翻訳が完了しました。")
    
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    similarity_pairs = list()
    
    i = 0
    with open(original, "r", encoding="utf-8") as f:
        for line_org in f:
            embeddings_org = model.encode(line_org, convert_to_tensor=True)
            similarity_pairs.append(list())
            for line_trans_in_target in trans_in_target:
                embedding_trans = model.encode(line_trans_in_target[1], convert_to_tensor=True)
                cosine_score = util.pytorch_cos_sim(embeddings_org, embedding_trans)[0][0]
                similarity_pairs[i].append([line_org, line_trans_in_target[0], cosine_score.detach().cpu().numpy().item()])
            i = i+1
    f.close()

    for i in similarity_pairs:
        print(find_max_similarity_pairs(i))
        print("\n")
    
    # 文章をベクトルに変換
    #embeddings1 = model.encode(sentence1, convert_to_tensor=True)
    #embeddings2 = model.encode(data2, convert_to_tensor=True)
    #embeddings3 = model.encode(sentence2, convert_to_tensor=True)

    # コサイン類似度の計算
    #cosine_score = util.pytorch_cos_sim(embeddings1, embeddings2)[0][0]
    #cosine_score2 = util.pytorch_cos_sim(embeddings3, embeddings2)[0][0]

    #print(f"類似度1: {cosine_score}")
    #print(f"類似度2: {cosine_score2}")


import pyttsx3

def speak_text(text, lang="en"):
    """ 指定されたテキストを音声で読み上げる """
    engine = pyttsx3.init()
    
    # 言語ごとに音声エンジンのプロパティを設定
    voices = engine.getProperty('voices')
    if lang == "fr":
        for voice in voices:
            if "french" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
    else:  # デフォルトは英語
        for voice in voices:
            if "english" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break

    engine.say(text)
    engine.runAndWait()
