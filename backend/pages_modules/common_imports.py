from backend.models import db, Users, Animals, Types, Categories, Posts, Pages
from bs4 import BeautifulSoup
import bleach
from flask import render_template, flash, redirect, abort, url_for, request