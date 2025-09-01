#!/bin/bash
exec celery -A tasks worker -B --loglevel=info