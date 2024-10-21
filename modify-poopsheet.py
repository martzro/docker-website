import psycopg2
from pydantic import BaseModel
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
import logging
from typing import Optional

# Configure the logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

# Create a logger instance
logger = logging.getLogger(__name__)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

origins = [
    "http://poopsheet.lol",
    "https://poopsheet.lol",
    "http://localhost",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class User(BaseModel):
    userid: int | str | None = None
    username: str | None = None
    email: str | None = None
    date: str | datetime = None
    is_active: bool | str = True

class Comment(BaseModel):
    poopid: int | str | None = None
    comment : str | None = None
    date : datetime  = datetime.now()

class Like(BaseModel):
    poopid : int | str | None
    date : datetime = datetime.now()

class Group(BaseModel):
    group_name: str = None
    groupid: int | str = "NEXTVAL('GROUPID')"
    date: datetime | str = datetime.now()

class Poop(BaseModel):
    rownum: int | str =  "NEXTVAL('POOPID')"
    comment: str | None = None
    date: datetime | str = datetime.now()
    is_retro: bool | str = False

class PoopEvent(BaseModel):
    event_type: str
    poop: Poop
    user: User
    group: Group
    like : Optional[Like] = None
    comment: Optional[Comment] = None

class DB:
    def __init__(self, database, host, user, password, port):
        self.conn = psycopg2.connect(database=database,
                            host=host,
                            user=user,
                            password=password,
                            port=port)
        self.curr = self.conn.cursor()
        self.success = {'status_code': 200, 'success': True}
     
    def query_db(self, query: str):

        self.curr.execute(query)

        return self.curr
    
    def add_user(self, user: User) -> bool:
        query = f"INSERT INTO USERS VALUES(NEXTVAL('USERID'), '{user.username}', '{user.email}');"

        try: 
            self.query_db(query)
        except Exception as e:
            self.query_db('rollback;')
            logger.error(f"ADD_USER ==> {user.username} Error {e}", exc_info=True)
            return 400
        else:
            self.query_db('commit;')
            logger.info(f"ADD_USER ==> User {user.username} Added")
            return self.success
        
    def update_user_status(self, user: User) -> bool:
        query = f"UPDATE USERS SET IS_ACTIVE = '{user.is_active}' WHERE USER_NAME = '{user.username}';"
        try: 
            self.query_db(query)
        except Exception as e:
            self.query_db('rollback;')
            logger.error(f"update_user_status ==> {user.username} to {user.is_active} Error {e}", exc_info=True)
            return 400
        else:
            self.query_db('commit;')
            logger.info(f"update_user_status ==> User {user.username} Updated to {user.is_active}")
            return True
        
    def add_group(self, group: Group) -> bool:
        self.set_group_id(group)
        if not group.groupid:
            group.groupid = "NEXTVAL('GROUPID')"
            query = f"INSERT INTO GROUPS VALUES('{group.group_name}', {group.groupid});"
            try: 
                self.query_db(query)
            except Exception as e:
                self.query_db('rollback;')
                logger.error(f"add_group ==> {group.group_name} Error {e}", exc_info=True)
                return 400

            else:
                self.query_db('commit;')
                logger.info(f"add_group ==> Added {group.group_name}")
                return self.success
        else:
            logger.error(f"add_group ==> {group.group_name} group already exists")
            return 401
        
    def set_user_info(self, user: User) -> None:
        query = f"SELECT USERID, EMAIL, DATE_ADDED FROM USERS WHERE USER_NAME = TRIM(LOWER('{user.username}')) AND EMAIL = TRIM(LOWER('{user.email}')) AND IS_ACTIVE = TRUE;"
        userInfo = self.query_db(query).fetchone()
        if userInfo:
            user.userid = userInfo[0] if not user.userid else user.userid
            user.email = userInfo[1] if not user.email else user.email
            user.date = userInfo[2] if not user.date else user.date
            
    def set_group_id(self, group: Group) -> None:
        query = f"SELECT GROUPID FROM GROUPS WHERE GROUPNAME = '{group.group_name}'"
        groupid = self.query_db(query).fetchone()
        
        group.groupid =  groupid[0] if groupid else None
    

    def add_user_to_group(self, user: User, group: Group) -> bool:
        self.set_user_info(user)
        self.set_group_id(group)

        #self.get_groups_where_user_is_member(user)

        if all([user.userid, group.groupid]):
            query = f"INSERT INTO GROUP_MEMBERS VALUES('{group.groupid}', '{user.userid}');"
            try: 
                
                self.query_db(query)
            except Exception as e:
                self.query_db('rollback;')
                logger.error(f"add_user_to_group ==> user {group.group_name} group {group.group_name} Error {e}", exc_info=True)
                return 400
            else:
                self.query_db('commit;')
                logger.info(f"add_user_to_group ==> Added {user.username} to {group.group_name}")
                return self.success
        else:
            logger.error(f"add_user_to_group ==> user {user.username} or group {group.group_name} not found")
            return 401
        
    def add_poop(self, poop: Poop, user: User):
        self.set_user_info(user)
        if user.userid:
            query = f"INSERT INTO POOPS VALUES(NEXTVAL('POOPID'), '{user.userid}', '{poop.comment}')" if not poop.date else f"INSERT INTO POOPS VALUES(NEXTVAL('POOPID'), '{user.userid}', '{poop.comment}','{poop.date}', {True})"
            try: 
                self.query_db(query)
            except Exception as e:
                self.query_db('rollback;')
                logger.error(f"add_poop ==> poop {poop} user {user} Error {e}", exc_info=True)
                return 400
            else:
                self.query_db('commit;')
                logger.info(f"add_poop ==> Added {poop} for user {user.username}")
                return self.success
        else:
            logger.error(f"add_poop ==> poop {poop} user {user} user not found", exc_info=True)
            return 401
        
    def login(self, user: User):
        self.set_user_info(user)
        if user.userid:
            logger.info(f"login ==> {user.username} logged in")
            return self.success
        else:
            logger.error(f"login ==> {user.username} not found")
            return 401
    
    def get_group_analytics_for_users_groups(self, user: User):
        self.set_user_info(user)

        if user.userid:
            try:
                query = f"""
                        WITH 
                            MEMBERS_GROUPS AS (
                            SELECT GROUPID FROM GROUP_MEMBERS WHERE USERID = {user.userid}
                            )
                        SELECT
                            G.GROUPNAME AS GROUP
                            , U.USER_NAME AS USER
                            , COUNT(*) AS POOP_COUNT
                        FROM
                            GROUPS G LEFT JOIN GROUP_MEMBERS GM ON G.GROUPID = GM.GROUPID
                            LEFT JOIN USERS U ON GM.USERID = U.USERID
                            INNER JOIN MEMBERS_GROUPS MG ON G.GROUPID = MG.GROUPID
                            INNER JOIN POOPS P ON U.USERID = P.USERID
                        WHERE
                            MG.GROUPID IS NOT NULL
                            AND P.DATE_ADDED > DATE_TRUNC('month', CURRENT_DATE)
                        GROUP BY
                            G.GROUPNAME
                            , U.USER_NAME
                        ORDER BY G.GROUPNAME, COUNT(*)
                        """
                
                results = self.query_db(query=query).fetchall()
            except Exception as e:
                logger.error(f"get_group_analytics_for_users_groups ==> {user.username} {e}", exc_info=True)
                return 400
            else:
                if results:
                    logger.info(f"get_group_analytics_for_users_groups ==> Returning analytics for {user.username}")
                    return [self.success, results]
                else:
                    logger.error(f"get_group_analytics_for_users_groups ==> query empty for user {user.username}")
                    return [401, []]
                
    def get_poops_from_group(self, user: User, group: Group):
        self.set_user_info(user)

        if user.userid:
            try:
                query = f"""
                        WITH G AS (
                        SELECT GROUPID, GROUPNAME FROM GROUPS WHERE GROUPNAME = '{group.group_name}'
                        )
                        SELECT
                            G.GROUPNAME AS GROUP
                            , U.USER_NAME AS USER
                            , P.COMMENT AS COMMENT
                            , TO_CHAR(P.DATE_ADDED, 'MM-DD-YY HH:MM:SS') AS DATE
                        FROM
                            G LEFT JOIN GROUP_MEMBERS GM ON G.GROUPID = GM.GROUPID
                            LEFT JOIN USERS U ON GM.USERID = U.USERID
                            INNER JOIN POOPS P ON U.USERID = P.USERID
                        WHERE
                            P.DATE_ADDED > DATE_TRUNC('month', CURRENT_DATE)
                        ORDER BY P.DATE_ADDED DESC
                        """
                
                results = self.query_db(query=query).fetchall()
            except Exception as e:
                logger.error(f"get_poops_from_group ==> {user.username} {e}", exc_info=True)
                return 400
            else:
                if results:
                    logger.info(f"get_poops_from_group ==> Returning groups poops for {user.username}")
                    return {'status_code': 200, 'success': True, 'submissions': [submission for submission in results]}
                else:
                    logger.error(f"get_poops_from_group ==> query empty for user {user.username}")
                    return [401, []]
    def get_groups_where_user_is_member(self, user: User):
        self.set_user_info(user)

        if user.userid:
            try:
                query = f"""
                        SELECT DISTINCT G.GROUPNAME FROM GROUP_MEMBERS GM, GROUPS G WHERE GM.USERID = {user.userid} AND GM.GROUPID=G.GROUPID
                        """
                
                results = self.query_db(query=query).fetchall()
            except Exception as e:
                logger.error(f"get_groups_where_user_is_member ==> {user.username} {e}", exc_info=True)
                return 400
            else:
                if results:
                    logger.info(f"get_groups_where_user_is_member ==> Returning groups for {user.username} ")
                    return  {'status_code': 200, 'success': True, 'groups': [group[0] for group in results]}
                else:
                    logger.error(f"get_groups_where_user_is_member ==> query empty for user {user.username}")
                    return [401, []]
                
    def get_poops_for_user(self, user: User):
        self.set_user_info(user)

        if user.userid:
            try:
                query = f"""
                        SELECT COUNT(*) FROM POOPS WHERE USERID = {user.userid} AND DATE_ADDED > DATE_TRUNC('month', CURRENT_DATE)
                        """
                
                results = self.query_db(query=query).fetchall()
            except Exception as e:
                logger.error(f"get_poops_for_user ==> {user.username} {e}", exc_info=True)
                return 400
            else:
                if results:
                    logger.info(f"get_poops_for_user ==> Returning poops for {user.username}")
                    return {'status_code': 200, 'success': True, 'count': results[0][0]}
                else:
                    logger.error(f"get_poops_for_user ==> query empty for user {user.username}")
                    return [401, []]
    def get_all_groups(self, user: User):
        self.set_user_info(user)

        if user.userid:
            try:
                query = f"""
                        SELECT DISTINCT GROUPNAME FROM GROUPS WHERE GROUPNAME IS NOT NULL ORDER BY GROUPNAME
                        """
                
                results = self.query_db(query=query).fetchall()
            except Exception as e:
                logger.error(f"get_all_groups ==> {user.username} {e}", exc_info=True)
                return 400
            else:
                if results:
                    logger.info(f"get_all_groups ==> Returning groups for {user.username}")
                    return {'status_code': 200, 'success': True, 'groups': [group[0] for group in results]}
                else:
                    logger.error(f"get_all_groups ==> query empty for user {user.username}")
                    return [401, []]
    def add_comment(self, comment: Comment, user: User):
        self.set_user_info(user)

        if user.userid:
            try:
                query = f"""
                        INSERT INTO COMMENTS (COMMENT, POOPID, USERID) VALUES('{comment.comment}',{comment.poopid} , {user.userid});
                        UPDATE POOPS SET COMMENT_COUNT = COMMENT_COUNT + 1 WHERE POOPID = {comment.poopid};
                        """
                
                results = self.query_db(query=query)
            except Exception as e:
                logger.error(f"add_comment ==> {user.username} {e}", exc_info=True)
                return 400
            else:
                if results:
                    logger.info(f"add_comment ==> updating comments for {comment.poopid}")
                    return self.success
                else:
                    logger.error(f"add_comment ==> query empty for user {user.username}")
                    return [401, []]
    
    def add_like(self, like: Like, user: User):
        self.set_user_info(user)

        if user.userid:
            try:
                query = f"""
                        INSERT INTO LIKES (POOPID, USERID) VALUES('{like.poopid} , {user.userid});
                        UPDATE POOPS SET LIKE_COUNT = LIKE_COUNT + 1 WHERE POOPID = {like.poopid};
                        """
                
                results = self.query_db(query=query)
            except Exception as e:
                logger.error(f"add_like ==> {user.username} {e}", exc_info=True)
                return 400
            else:
                if results:
                    logger.info(f"add_like ==> added like for {like.poopid}")
                    return self.success
                else:
                    logger.error(f"add_like ==> query empty for user {user.username}")
                    return 400


            


@app.post("/api/event")
def main(poopevent: PoopEvent):
    db = DB('poop-sheet', 'db', 'postgres', 'postgres', '5432')

    event_type = poopevent.event_type
    print(poopevent)

    match event_type:
        case 'log-poop':
            return db.add_poop(poopevent.poop, poopevent.user)
        case 'add-user':
            return db.add_user(poopevent.user)
        case 'add-user-to-group':
           return db.add_user_to_group(poopevent.user, poopevent.group)
        case 'add-group':
            return db.add_group(poopevent.group)
        case 'login':
            return db.login(poopevent.user)
        case 'get-group-analytics':
            return db.get_group_analytics_for_users_groups(poopevent.user)
        case 'get-groups-user-is-in':
            return db.get_groups_where_user_is_member(poopevent.user)
        case 'get-poops-from-group':
            return db.get_poops_from_group(poopevent.user, poopevent.group)
        case 'get-poops-for-user':
            return db.get_poops_for_user(poopevent.user)
        case 'get-all-groups':
            return db.get_all_groups(poopevent.user)
        case 'add-comment':
            return db.add_comment(poopevent.comment, poopevent.user)
        case 'add-like':
            return db.add_like(poopevent.like, poopevent.user)
        case _:
            return 


@app.get("/", response_class=HTMLResponse)
async def get_login():
    html_content = Path("login.html").read_text()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/summary", response_class=HTMLResponse)
async def get_login():
    html_content = Path("summary.html").read_text()
    return HTMLResponse(content=html_content, status_code=200)