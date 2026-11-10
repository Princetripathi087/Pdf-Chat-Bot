from pymongo import mongo_client
import pymongo
from app.config import settings
import os
from typing import Dict, List
import dotenv
import pandas as pd
import numpy as np
from tqdm import tqdm


connection_options = {
    "retryWrites": "true",
    "w": "majority"
}

client = mongo_client.MongoClient(
    settings.DATABASE_URL_VECTOR,**connection_options)


try:
    conn = client.server_info()
    print(f'Connected to MongoDB {conn.get("version")}')
except Exception:
    print("Unable to connect to the MongoDB server.")

db = client[settings.MONGO_INITDB_DATABASE]
User = db.users
User.create_index([("email", pymongo.ASCENDING)], unique=True)

EMBEDDING_COLLECTION = "EMBEDDING_COLLECTION"
GRC_EMBEDDING_COLLECTION="GRC_EMBEDDING_COLLECTION"
CHATBOT_EMBEDDING_COLLECTION="CHATBOT_EMBEDDING_COLLECTION"
CONTROL_MAP_EMBEDDING_COLLECTION="CONTROL_MAP_EMBEDDING_COLLECTION"
IMAGE_COLLECTION = "image_embed"
CONTRACT_COLLECTION = "CONTRACT_EMBED"
DOCUMENT_COLLECTION = "DOC_COLLECTION"
TPRM_MENDIX_DATABASE="TPRM_MENDIX_DATABASE"



def normalized_score(df):
    if len(df) == 0:
        df['normalized_score'] = None
        return df
    max_score = max(df['score'])
    min_score = min(df['score'])
    if (max_score-min_score) == 0:
        df['normalized_score'] = df['score']
    else:
        df['normalized_score'] = df['score'].apply(
            lambda x: (x-min_score)/(max_score-min_score))
    return df


def combine_vector_keyword_search(vector_search_results, keyword_search_results, limit: int = 5):

    if len(vector_search_results) == 0 and len(keyword_search_results) == 0:
        return []

    df_keyword_search = pd.DataFrame(keyword_search_results)
    df_vector_search = pd.DataFrame(vector_search_results)

    if len(vector_search_results) == 0:
        results = df_keyword_search.to_dict(orient='records')
        return results

    if len(keyword_search_results) == 0:
        results = df_vector_search.to_dict(orient='records')
        return results

    both_hit_indices = set(df_vector_search[['textIdx']].merge(
        df_keyword_search[['textIdx']])['textIdx'])

    rest_size = limit - len(both_hit_indices)

    df_vector_search = normalized_score(df_vector_search)
    df_keyword_search = normalized_score(df_keyword_search)

    df_hybrid_search = pd.concat([df_keyword_search, df_vector_search])

    df_hybrid_search_1 = df_keyword_search[df_keyword_search['textIdx'].isin(
        both_hit_indices)].copy()

    df_hybrid_search_1['both_hit'] = True
    df_hybrid_search_2 = df_hybrid_search[~df_hybrid_search['textIdx'].isin(
        both_hit_indices)].copy()

    df_hybrid_search_2 = df_hybrid_search_2.sort_values(
        by='normalized_score', ascending=False).head(rest_size)
    df_hybrid_search_2['both_hit'] = False

    df_hybrid_search = pd.concat([df_hybrid_search_1, df_hybrid_search_2])

    results = df_hybrid_search.to_dict(orient='records')

    return results

def image_combine_vector_keyword_search(self, vector_results: List[Dict], keyword_results: List[Dict], limit: int) -> List[Dict]:
        # Combine and deduplicate results based on fileName
        combined_results = {res['fileName']: res for res in vector_results + keyword_results}

        # Sort results by score and limit the number of results
        sorted_results = sorted(combined_results.values(), key=lambda x: x.get('score', 0), reverse=True)
        return sorted_results[:limit]


class MongoDB():

    def __init__(self) -> None:
        self.client = client 
        self.db = self.client[settings.MONGO_INITDB_DATABASE]

    def file_exist(self, file_name: str) -> bool:
        collection = self.db[DOCUMENT_COLLECTION]
        results = collection.find_one({"fileName": file_name})
        return results is not None
    
    def url_exist(self, url:str) -> bool:
        collection = self.db[DOCUMENT_COLLECTION]
        results = collection.find_one({"domain": url})
        return results is not None

    def insert_document(self, file_name: str):
        collection = self.db[DOCUMENT_COLLECTION]
        collection.insert_one(
            {'fileName': file_name,
             "fileUrl": f"https://baarez.net/rag-documents/{file_name}"})

    def insert_url(self, url: str):
        collection = self.db[DOCUMENT_COLLECTION]
        collection.insert_one(
            {"domain": url})

    def insert_embedding(self, doc_meta_list) -> List:
        collection = self.db[EMBEDDING_COLLECTION]
        collection.insert_many(doc_meta_list)
        
    def insert_mendix_embedding(self, doc_meta_list) -> List:
        collection = self.db[TPRM_MENDIX_DATABASE]
        collection.insert_many(doc_meta_list)
    
    def insert_grc_embedding(self, doc_meta_list) -> List:
        collection = self.db[GRC_EMBEDDING_COLLECTION]
        collection.insert_many(doc_meta_list)
        
    def insert_chatbot_embedding(self, doc_meta_list) -> List:
        collection = self.db[CHATBOT_EMBEDDING_COLLECTION]
        collection.insert_many(doc_meta_list)
        
    def insert_control_map_embedding(self, doc_meta_list) -> List:
        collection = self.db[CONTROL_MAP_EMBEDDING_COLLECTION]
        collection.insert_many(doc_meta_list)
    
    def image_insert_embedding(self, doc_meta_list) -> List:
        collection = self.db[IMAGE_COLLECTION]
        collection.insert_many(doc_meta_list)
    
    def contract_insert_embedding(self, doc_meta_list) -> List:
        collection = self.db[CONTRACT_COLLECTION]
        collection.insert_many(doc_meta_list)
        
    def cosine_similarity(self,a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
    def compute_similarity(self, vector1: List[float], vector2: List[float]) -> float:
        """Compute the cosine similarity between two vectors."""
        v1 = np.array(vector1)
        v2 = np.array(vector2)
        cos_sim = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        return cos_sim
    
    def control_vector_search(self, query_vector: List[float],limit: int = 5) -> List[Dict]:
        results = self.db[CONTROL_MAP_EMBEDDING_COLLECTION].aggregate([
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "path": "embedding",
                    "queryVector": query_vector,
                    "numCandidates": limit,
                    "limit": limit,
                }
            },
            {
                "$project": {
                    "embedding": 0,
                    "_id": 0,
                    "score": {"$meta": "vectorSearchScore"}
                }
            }
        ])
        return list(results)
        
        
    def vector_search(self, query_vector: List[float], user_id: str, limit: int = 5) -> List[Dict]:
        if len(user_id)>0:
            results = self.db[EMBEDDING_COLLECTION].aggregate([
                {
                    "$vectorSearch": {
                        "index": "vector_index",
                        "path": "embedding",
                        "queryVector": query_vector,
                        "numCandidates": limit,
                        "limit": limit,
                        "filter": {
                            "user_id": user_id  # Limited filtering capabilities
                        }
                    }
                },
                {
                    "$project": {
                        "embedding": 0,
                        "_id": 0,
                        "score": {"$meta": "vectorSearchScore"}
                    }
                }
            ])
            return list(results)  
        else:
            results = self.db[EMBEDDING_COLLECTION].aggregate([
                {

                    "$vectorSearch": {
                        "index": "vector_index",
                        "path": "embedding",
                        "queryVector": query_vector,
                        "numCandidates": limit,
                        "limit": limit
                    },  

                },             
                {

                    '$project': {
                        'embedding': 0,
                        "_id": 0,
                        "score": {"$meta": "vectorSearchScore"},
                    }

                }

            ])
            
            return list(results)
        
        
    def chatbot_vector_search(self, query_vector: List[float],limit: int = 5) -> List[Dict]:
        results = self.db[CHATBOT_EMBEDDING_COLLECTION].aggregate([
            {

                "$vectorSearch": {
                    "index": "vector_index",
                    "path": "embedding",
                    "queryVector": query_vector,
                    "numCandidates": limit,
                    "limit": limit
                },  

            },             
            {

                '$project': {
                    'embedding': 0,
                    "_id": 0,
                    "score": {"$meta": "vectorSearchScore"},
                }

            }

        ])
        
        return list(results)
        
    def mendix_vector_search(self, query_vector: List[float],limit: int = 5) -> List[Dict]:
        results = self.db[TPRM_MENDIX_DATABASE].aggregate([
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "path": "embedding",
                    "queryVector": query_vector,
                    "numCandidates": limit,
                    "limit": limit,
                }
            },
            {
                "$project": {
                    "embedding": 0,
                    "_id": 0,
                    "score": {"$meta": "vectorSearchScore"}
                }
            }
        ])
        return list(results)
            
    def contract_vector_search(self, query_vector: List[float],file_name:str, limit: int = 5) -> List[Dict]:

        results = self.db[CONTRACT_COLLECTION].aggregate([
            {

                "$vectorSearch": {
                    "index": "contract_vector_index",
                    "path": "embedding",
                    "queryVector": query_vector,
                    "numCandidates": limit,
                    "limit": limit,
                     "filter": {
                    "fileName": file_name
                }
                    
                }

            },
             
            {

                '$project': {
                    'embedding': 0,
                    "_id": 0,
                    "score": {"$meta": "vectorSearchScore"},
                }

            }

        ])
        return list(results)
    
    def grc_vector_search(self, query_vector: List[float], user_id: str,policy_id:str,doc_type:str, limit: int = 5) -> List[Dict]:
        if len(user_id)>0:
            results = self.db[GRC_EMBEDDING_COLLECTION].aggregate([
                {
                    "$vectorSearch": {
                        "index": "vector_index",
                        "path": "embedding",
                        "queryVector": query_vector,
                        "numCandidates": limit,
                        "limit": limit,
                        "filter": {
                            "user_id": user_id,# Limited filtering capabilities
                            # "file_code": policy_id,
                            "doc_type": doc_type
                        }
                    }
                },
                {
                    "$project": {
                        "embedding": 0,
                        "_id": 0,
                        "score": {"$meta": "vectorSearchScore"}
                    }
                }
            ])
            return list(results)
            # filtered_docs = list(self.db[EMBEDDING_COLLECTION].find({'user_id': user_id}))
            
            # similarities = []
            # for s_doc in tqdm(filtered_docs):
            #     similarities.append({"_id":s_doc["_id"],
            #                     "fileName":s_doc["fileName"],
            #                     "textIdx":s_doc["textIdx"],
            #                     "pageLabel":s_doc["pageLabel"],
            #                     "text":s_doc["text"],
            #                     "user_id":s_doc["user_id"],
            #                     "embedding": s_doc["embedding"],
            #                     "score": self.cosine_similarity(query_vector, s_doc['embedding'])})
                
                
            # similarities.sort(key=lambda x: x["score"], reverse=True)
            
            # return similarities[:limit]
        
        else:
            results = self.db[GRC_EMBEDDING_COLLECTION].aggregate([
                {

                    "$vectorSearch": {
                        "index": "vector_index",
                        "path": "embedding",
                        "queryVector": query_vector,
                        "numCandidates": limit,
                        "limit": limit
                    },  

                },             
                {

                    '$project': {
                        'embedding': 0,
                        "_id": 0,
                        "score": {"$meta": "vectorSearchScore"},
                    }

                }

            ])
            
            return list(results)
        
    def grc_selfassesment_vector_search(self, query_vector: List[float], user_id: str,doc_type:str, limit: int = 5) -> List[Dict]:
        if len(user_id)>0:
            results = self.db[GRC_EMBEDDING_COLLECTION].aggregate([
                {
                    "$vectorSearch": {
                        "index": "vector_index",
                        "path": "embedding",
                        "queryVector": query_vector,
                        "numCandidates": limit,
                        "limit": limit,
                        "filter": {
                            "user_id": user_id,# Limited filtering capabilities
                            # "file_code": policy_id,
                            "doc_type": doc_type
                        }
                    }
                },
                {
                    "$project": {
                        "embedding": 0,
                        "_id": 0,
                        "score": {"$meta": "vectorSearchScore"}
                    }
                }
            ])
            return list(results)
        else:
            results = self.db[GRC_EMBEDDING_COLLECTION].aggregate([
                {

                    "$vectorSearch": {
                        "index": "vector_index",
                        "path": "embedding",
                        "queryVector": query_vector,
                        "numCandidates": limit,
                        "limit": limit
                    },  

                },             
                {

                    '$project': {
                        'embedding': 0,
                        "_id": 0,
                        "score": {"$meta": "vectorSearchScore"},
                    }

                }

            ])
            
            return list(results)
        
    def grc_evidence_vector_search(self, query_vector: List[float], user_id: str,evidence_id:str,doc_type:str, limit: int = 5) -> List[Dict]:
        if len(user_id)>0:
            results = self.db[GRC_EMBEDDING_COLLECTION].aggregate([
                {
                    "$vectorSearch": {
                        "index": "vector_index",
                        "path": "embedding",
                        "queryVector": query_vector,
                        "numCandidates": limit,
                        "limit": limit,
                        "filter": {
                            "user_id": user_id,# Limited filtering capabilities
                            "file_code": evidence_id,
                            "doc_type": doc_type
                        }
                    }
                },
                {
                    "$project": {
                        "embedding": 0,
                        "_id": 0,
                        "score": {"$meta": "vectorSearchScore"}
                    }
                }
            ])
            return list(results)
        else:
            results = self.db[GRC_EMBEDDING_COLLECTION].aggregate([
                {

                    "$vectorSearch": {
                        "index": "vector_index",
                        "path": "embedding",
                        "queryVector": query_vector,
                        "numCandidates": limit,
                        "limit": limit
                    },  

                },             
                {

                    '$project': {
                        'embedding': 0,
                        "_id": 0,
                        "score": {"$meta": "vectorSearchScore"},
                    }

                }

            ])
            
            return list(results)
    

    def image_vector_search(self, query_vector: List[float], limit: int = 5) -> List[Dict]:
        results = self.db["image_embed"].aggregate([
            {
                "$vectorSearch": {
                    "index": "image_vector_index",
                    "path": "embedding",
                    "queryVector": query_vector,
                    "numCandidates": limit,
                    "limit": limit
                }
            },
            {
                '$project': {
                    'embedding': 0,
                    "_id": 0,
                    "score": {"$meta": "vectorSearchScore"},
                }
            }
        ])
        return list(results)

    def keyword_search(self, query: str, limit: int = 5) -> List[Dict]:

        search_query = [
            {
                '$search': {
                    'index': 'default',
                    'compound': {
                        'must': [
                            {
                                'text': {
                                    'query': query,
                                    'path': 'text'
                                }
                            }
                        ]
                    }
                }
            },
             {
                '$addFields': {
                    'score': {
                        '$meta': 'searchScore'
                    }
                }
            }, {
                '$project': {
                    'embedding': 0
                }
            }, {
                '$limit': limit
            }
        ]

        results = self.db[EMBEDDING_COLLECTION].aggregate(search_query)

        return list(results)
    
    def chatbot_keyword_search(self, query: str, limit: int = 5) -> List[Dict]:

        search_query = [
            {
                '$search': {
                    'index': 'default',
                    'compound': {
                        'must': [
                            {
                                'text': {
                                    'query': query,
                                    'path': 'text'
                                }
                            }
                        ]
                    }
                }
            },
             {
                '$addFields': {
                    'score': {
                        '$meta': 'searchScore'
                    }
                }
            }, {
                '$project': {
                    'embedding': 0
                }
            }, {
                '$limit': limit
            }
        ]

        results = self.db[CHATBOT_EMBEDDING_COLLECTION].aggregate(search_query)

        return list(results)
    
    def mendix_keyword_search(self, query: str, limit: int = 5) -> List[Dict]:

        search_query = [
            {
                '$search': {
                    'index': 'default',
                    'compound': {
                        'must': [
                            {
                                'text': {
                                    'query': query,
                                    'path': 'text'
                                }
                            }
                        ]
                    }
                }
            },
             {
                '$addFields': {
                    'score': {
                        '$meta': 'searchScore'
                    }
                }
            }, {
                '$project': {
                    'embedding': 0
                }
            }, {
                '$limit': limit
            }
        ]

        results = self.db[TPRM_MENDIX_DATABASE].aggregate(search_query)

        return list(results)
    
    def control_keyword_search(self, query: str, limit: int = 5) -> List[Dict]:

        search_query = [
            {
                '$search': {
                    'index': 'default',
                    'compound': {
                        'must': [
                            {
                                'text': {
                                    'query': query,
                                    'path': 'text'
                                }
                            }
                        ]
                    }
                }
            },
             {
                '$addFields': {
                    'score': {
                        '$meta': 'searchScore'
                    }
                }
            }, {
                '$project': {
                    'embedding': 0
                }
            }, {
                '$limit': limit
            }
        ]

        results = self.db[CONTROL_MAP_EMBEDDING_COLLECTION].aggregate(search_query)

        return list(results)
    
    def grc_keyword_search(self, query: str, limit: int = 5) -> List[Dict]:

        search_query = [
            {
                '$search': {
                    'index': 'default',
                    'compound': {
                        'must': [
                            {
                                'text': {
                                    'query': query,
                                    'path': 'text'
                                }
                            }
                        ]
                    }
                }
            },
             {
                '$addFields': {
                    'score': {
                        '$meta': 'searchScore'
                    }
                }
            }, {
                '$project': {
                    'embedding': 0
                }
            }, {
                '$limit': limit
            }
        ]

        results = self.db[GRC_EMBEDDING_COLLECTION].aggregate(search_query)

        return list(results)

    def image_keyword_search(self, query: str, limit: int = 5) -> List[Dict]:
            results = self.db["image_embed"].find(
                {"$text": {"$search": query}},
                {"score": {"$meta": "textScore"}, "_id": 0, "embedding": 0}
            ).sort([("score", {"$meta": "textScore"})]).limit(limit)
            return list(results)
    
    def hybrid_search(self, query_vector: List[float], query: str,user_id:str, limit: int = 5) -> List[Dict]:
        vector_search_results = self.vector_search(query_vector=query_vector,user_id=user_id, limit=limit)

        keyword_search_results = self.keyword_search(query=query,
                                                     limit=limit)

        hybrid_search_results = combine_vector_keyword_search(
            vector_search_results, keyword_search_results, limit=limit)

        return hybrid_search_results
    
    def chatbot_hybrid_search(self, query_vector: List[float], query: str, limit: int = 5) -> List[Dict]:
        vector_search_results = self.chatbot_vector_search(query_vector=query_vector, limit=limit)

        keyword_search_results = self.chatbot_keyword_search(query=query,
                                                     limit=limit)

        hybrid_search_results = combine_vector_keyword_search(
            vector_search_results, keyword_search_results, limit=limit)

        return hybrid_search_results
    

    
    def mendix_hybrid_search(self, query_vector: List[float], query: str,limit: int = 10) -> List[Dict]:
        vector_search_results = self.mendix_vector_search(query_vector=query_vector,limit=limit)
        keyword_search_results = self.mendix_keyword_search(query=query,
                                                     limit=limit)
        hybrid_search_results = combine_vector_keyword_search(
            vector_search_results, keyword_search_results, limit=limit)

        return vector_search_results
    
    def control_hybrid_search(self, query_vector: List[float], query: str, limit: int = 5) -> List[Dict]:
        vector_search_results = self.control_vector_search(query_vector=query_vector,limit=limit)

        keyword_search_results = self.control_keyword_search(query=query,
                                                     limit=limit)

        hybrid_search_results = combine_vector_keyword_search(
            vector_search_results, keyword_search_results, limit=limit)

        return vector_search_results
    
    def grc_evidence_hybrid_search(self, query_vector: List[float], query: str,user_id:str,evidence_id:str,doc_type:str, limit: int = 5) -> List[Dict]:
        vector_search_results = self.grc_evidence_vector_search(query_vector=query_vector,user_id=user_id,evidence_id=evidence_id,doc_type=doc_type,limit=limit)

        keyword_search_results = self.grc_keyword_search(query=query,
                                                     limit=limit)

        hybrid_search_results = combine_vector_keyword_search(
            vector_search_results, keyword_search_results, limit=limit)

        return hybrid_search_results
    
    def grc_hybrid_search(self, query_vector: List[float], query: str,user_id:str,policy_id:str,doc_type:str, limit: int = 5) -> List[Dict]:
        vector_search_results = self.grc_vector_search(query_vector=query_vector,user_id=user_id,policy_id=policy_id,doc_type=doc_type,limit=limit)

        keyword_search_results = self.grc_keyword_search(query=query,
                                                     limit=limit)

        hybrid_search_results = combine_vector_keyword_search(
            vector_search_results, keyword_search_results, limit=limit)

        return hybrid_search_results
    
    def grc_selfassesment_hybrid_search(self, query_vector: List[float], query: str,user_id:str,doc_type:str, limit: int = 5) -> List[Dict]:
        vector_search_results = self.grc_selfassesment_vector_search(query_vector=query_vector,user_id=user_id,doc_type=doc_type,limit=limit)

        keyword_search_results = self.grc_keyword_search(query=query,
                                                     limit=limit)

        hybrid_search_results = combine_vector_keyword_search(
            vector_search_results, keyword_search_results, limit=limit)

        return hybrid_search_results
    
    def contract_hybrid_search(self, query_vector: List[float],file_name:str, query: str, limit: int = 5) -> List[Dict]:
        vector_search_results = self.contract_vector_search(query_vector=query_vector,file_name=file_name ,limit=limit)

        keyword_search_results = self.keyword_search(query=query,
                                                     limit=limit)

        hybrid_search_results = combine_vector_keyword_search(
            vector_search_results, keyword_search_results, limit=limit)

        return hybrid_search_results
    
    def image_hybrid_search(self, query_vector: List[float], query: str, limit: int = 5) -> List[Dict]:
        vector_search_results = self.image_vector_search(query_vector=query_vector, limit=limit)
        keyword_search_results = self.image_keyword_search(query=query, limit=limit)
        hybrid_search_results = image_combine_vector_keyword_search(vector_search_results, keyword_search_results, limit=limit)
        return hybrid_search_results
