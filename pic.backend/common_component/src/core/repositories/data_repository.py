"""
Establish a connection to an RDS database using a proxy.

This function connects to an RDS database through an RDS proxy, generates
temporary token for IAM Authorization.
The function connects to the RDS database

Note:
- Make sure the necessary configuration for RDS proxy, RDS host, port, and username
    are set before calling this function.
"""

import boto3
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..utils.Config import config
from sqlalchemy.orm import Session
from sqlalchemy import event
from sqlalchemy.exc import SQLAlchemyError
import traceback
from common_component.src.core.utils.Logger import logger
from common_component.src.core.resources.constants import SELECT_QUERY
from contextlib import contextmanager

file_path = config.RDS_PROXY_SSL_CERTIFICATE_NAME
rds_proxy_host = config.APP_HOST
rds_port = config.APP_PORT
rds_username = config.RDS_PROXY_USERNAME
rds_ssl_certificate_name = config.RDS_PROXY_SSL_CERTIFICATE_NAME
rds_database = config.RDS_DATABASE
rds_proxy_reader_host = config.READER_DB_URL
rds_proxy_writer_host = config.WRITER_DB_URL


def read_file():
    """
    Check whether file is present in directory or not.
    """
    try:
        with open(file_path) as file:
            file.read()
            return True
    except FileNotFoundError:
        return False


read_file_flag = read_file()


class CreateDBConnection:
    def rds_proxy_connection_v1(self, rds_proxy):
        """
        Creates token for IAM Authorization.
        """
        token = boto3.client('rds').generate_db_auth_token(
            DBHostname=rds_proxy,
            Port=rds_port,
            DBUsername=rds_username
        )
        return token

    def create_sqlalchemy_engine_v1(self, rds_proxy):
        """
        Creates engine.
        """
        protocol = "postgresql+psycopg2"
        database = rds_database
        conn_str = f"{protocol}://{rds_proxy}:{rds_port}/{database}"
        engine = create_engine(conn_str)

        @event.listens_for(engine, "do_connect")
        def provide_token(dialect, conn_rec, cargs, cparams):
            """
            Updates token for IAM authentication in runtime.
            """
            token = self.rds_proxy_connection_v1(rds_proxy)
            cparams['user'] = rds_username
            cparams['password'] = token
            cparams['sslmode'] = 'verify-full'
            cparams['sslrootcert'] = file_path

        return engine

    @contextmanager
    def create_reader_connection(self):
        rds_proxy_engine = self.create_sqlalchemy_engine_v1(rds_proxy_reader_host)
        Session = sessionmaker(autoflush=False, bind=rds_proxy_engine)
        session = Session()

        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @contextmanager
    def create_writer_connection(self):
        rds_proxy_engine = self.create_sqlalchemy_engine_v1(rds_proxy_writer_host)
        Session = sessionmaker(autoflush=False, bind=rds_proxy_engine)
        session = Session()

        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()


Base = declarative_base()


def call_postgres_function(query, parameters=None, db: Session = None):
    """
    This is a generic definition to call postgres functions.
    """
    try:
        if parameters is not None:
            function_parameters = parameters
            result = db.execute(query, function_parameters)
        else:
            result = db.execute(query)
        if SELECT_QUERY in str(query).lower():
            output = result.mappings().all()
        else:
            output = result

        return output

    except SQLAlchemyError as e:
        # Catch and handle SQLAlchemy errors
        if hasattr(e, 'orig') and hasattr(e.orig, 'pgcode'):
            postgres_error_code = e.orig.pgcode
            logger.info("Raise exception is raised")
            raise e
        else:
            # Handle other SQLAlchemy errors
            logger.info("SQL Alchemy exception raised")
            raise e
    except Exception as err:
        traceback.print_exc()
        # pass exception to function
        logger.info("error is caught in root exception")
        raise err

# import boto3
# from sqlalchemy import create_engine, exc
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, Session
# from ..utils.Local_Config import config
# from fastapi import Depends, HTTPException, status, Response
# from sqlalchemy.exc import SQLAlchemyError
# import traceback
# from common_component.src.core.utils.Logger import logger
# from common_component.resources.constants import SELECT_QUERY
# from contextlib import contextmanager
#
# rds_proxy_host = config.APP_HOST
# rds_port = config.APP_PORT
# rds_username = config.RDS_PROXY_USERNAME
# rds_database = config.RDS_DATABASE
#
# engine = create_engine(rds_proxy_host, echo=True)
# session_local = sessionmaker(autoflush=False, bind=engine)
#
#
# class CreateDBConnection:
#
#     @contextmanager
#     def create_reader_connection(self):
#         engine = create_engine(rds_proxy_host, echo=True)
#         Session = sessionmaker(autoflush=False, bind=engine)
#         session = Session()
#
#         try:
#             yield session
#             session.commit()
#         except Exception as e:
#             session.rollback()
#             raise e
#         finally:
#             session.close()
#
#     @contextmanager
#     def create_writer_connection(self):
#         engine = create_engine(rds_proxy_host, echo=True)
#         Session = sessionmaker(autoflush=False, bind=engine)
#         session = Session()
#
#         try:
#             yield session
#             session.commit()
#         except Exception as e:
#             session.rollback()
#             raise e
#         finally:
#             session.close()
#
#
# Base = declarative_base()
#
#
# def call_postgres_function(query, parameters=None, db: Session = None):
#     """
#     This is a generic definition to call postgres functions.
#     """
#     try:
#         if parameters is not None:
#             function_parameters = parameters
#             result = db.execute(query, function_parameters)
#         else:
#             result = db.execute(query)
#         if SELECT_QUERY in str(query).lower():
#             output = result.mappings().all()
#         else:
#             output = result
#
#         return output
#
#     except SQLAlchemyError as e:
#         # Catch and handle SQLAlchemy errors
#         if hasattr(e, 'orig') and hasattr(e.orig, 'pgcode'):
#             postgres_error_code = e.orig.pgcode
#             logger.info("Raise exception is raised")
#             raise e
#         else:
#             # Handle other SQLAlchemy errors
#             logger.info("SQL Alchemy exception raised")
#             raise e
#     except HTTPException as http_exception:
#         # If it's a FastAPI HTTPException, re-raise it
#         raise http_exception
#     except Exception as err:
#         traceback.print_exc()
#         # pass exception to function
#         logger.info("error is caught in root exception")
#         raise err
#
