# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import pandas as pd
import streamlit as st
from streamlit.logger import get_logger
from tempfile import NamedTemporaryFile
from io import StringIO
import boto3

LOGGER = get_logger(__name__)


def affichage(row):
    col1,col2 = st.columns([0.12,0.88])
    with col1:
        st.write(row.Date)
    with col2:
        st.markdown(f"<a style='color: #31333f ; text-decoration: none;' href='https://{row.Lien}' target='_blank'>**{row.Titre}**</a>", unsafe_allow_html=True)   
        st.caption(row.Description)


def run():
    st.set_page_config(
        page_title="Base Presse AFA",
        page_icon="",
    )

    s3 = boto3.client('s3', aws_access_key_id=st.secrets['AWS_ACCESS_KEY_ID'], aws_secret_access_key=st.secrets['AWS_SECRET_ACCESS_KEY'])
    response = s3.get_object(Bucket='base-presse-afa', Key='bp.csv')
    df = pd.read_csv(StringIO(response['Body'].read().decode('utf-8')))

    st.header('Base Presse AFA')

    mots_clefs = st.text_input('Mots clefs :','').split()

    col1,col2 = st.columns(2)
    with col1:
        date_1 = st.date_input('Du :',datetime.date(2023,1,1),format="DD/MM/YYYY")
    with col2:
        date_2 = st.date_input('Au :',datetime.datetime.now(),format="DD/MM/YYYY")
    
    result = df[pd.to_datetime(df.Date, format=r'%d/%m/%Y').map(lambda x: x.date()).between(date_1,date_2)]
    for mot in mots_clefs:
        result = result[result.Titre.str.contains(mot,case=False)]
    result.apply(affichage,axis=1)

if __name__ == "__main__":
    run()
