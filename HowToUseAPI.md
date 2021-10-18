## API

## MOVIE

```
/movie/{id} : id를 가지는 영화
/movie : 모든영화
/search/movie/{str} : str을 제목이나 키워드에 포함하는 영화 검색
```

## BOARD

```
/board : get -모든 게시판 
/board : post -게시판 생성
/board/{id} : get -id=id인 게시판 불러오기
/board/{id} : put -id=id인 게시판 수정
/board/{id} : delete -id=id인 게시판 삭제
{
	# TYPE_CHOICES = (('1', 'FreeBoard'), ('2', 'review'))
	type(int)
	author(int) => user.id(foreignkey)
    title(str)
    content(str)
}

```

