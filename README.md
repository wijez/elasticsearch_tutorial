# elasticsearch_tutorial


Elasticsearch là một công cụ tìm kiếm và phân tích dữ liệu mã nguồn mở, dựa trên Apache Lucene. Nó được thiết kế để dễ dàng mở rộng và có khả năng tìm kiếm, phân tích dữ liệu cực kỳ nhanh chóng. Elasticsearch thường được sử dụng cho các trường hợp như tìm kiếm toàn văn, phân tích nhật ký, phân tích dữ liệu thời gian thực, và nhiều ứng dụng khác.

Mô hình cấu trúc và cách vận hành của Elasticsearch
1. Cluster (Cụm)
Cluster là tập hợp các nút (nodes) cùng làm việc với nhau, lưu trữ toàn bộ dữ liệu và cung cấp khả năng tìm kiếm và phân tích dữ liệu trên tất cả các nút. Mỗi cluster được xác định bởi một tên duy nhất và mặc định là "elasticsearch".

2. Node (Nút)
Node là một máy chủ đơn lẻ thuộc cluster. Mỗi node lưu trữ dữ liệu và tham gia vào quá trình tìm kiếm và phân tích dữ liệu. Mỗi node có một tên duy nhất và mặc định được tự động tạo ra khi node khởi động.

3. Index (Chỉ mục)
Index là một tập hợp các tài liệu (documents) có đặc điểm tương tự nhau. Mỗi index được xác định bởi một tên và được sử dụng để tham chiếu đến các tài liệu trong index đó.

4. Document (Tài liệu)
Document là đơn vị nhỏ nhất của dữ liệu có thể được lập chỉ mục trong Elasticsearch. Mỗi document là một đối tượng JSON và được lưu trữ trong một index. Mỗi document có một ID duy nhất.

5. Shard (Phân mảnh)
Index có thể quá lớn để phù hợp với một node duy nhất, vì vậy Elasticsearch chia nhỏ mỗi index thành nhiều mảnh nhỏ hơn được gọi là shard. Mỗi shard là một instance hoàn chỉnh và độc lập của Lucene, lưu trữ một phần của dữ liệu và có thể được di chuyển giữa các node trong cluster.

6. Replica (Bản sao)
Để đảm bảo tính khả dụng và độ tin cậy, mỗi shard có thể có một hoặc nhiều bản sao (replica). Replica không chỉ cung cấp khả năng dự phòng nếu một node bị lỗi, mà còn cải thiện khả năng tìm kiếm bằng cách phân phối tải tìm kiếm trên nhiều node.

Cách vận hành của Elasticsearch
Phân tán và Khả năng chịu lỗi

Elasticsearch được thiết kế để phân tán và chịu lỗi, với khả năng mở rộng ngang (horizontal scalability). Các index được chia thành nhiều shard và mỗi shard có thể có nhiều bản sao (replica) để đảm bảo tính sẵn sàng cao.

Tìm kiếm và Phân tích

Elasticsearch sử dụng các thuật toán tìm kiếm và phân tích tiên tiến của Lucene để cung cấp các tính năng tìm kiếm toàn văn (full-text search), tìm kiếm theo từ khóa, tìm kiếm fuzzy, tìm kiếm phạm vi, và nhiều loại tìm kiếm khác. Nó cũng cung cấp các tính năng phân tích dữ liệu như aggregation và pipeline aggregation để phân tích và tổng hợp dữ liệu.

RESTful API

Elasticsearch cung cấp một API RESTful mạnh mẽ, cho phép người dùng tương tác với cluster, index, và document thông qua các HTTP requests. Điều này làm cho Elasticsearch dễ dàng tích hợp với các ứng dụng web và các dịch vụ khác.

Realtime và Gần-realtime (NRT)

Elasticsearch được thiết kế để hỗ trợ tìm kiếm và cập nhật dữ liệu gần thời gian thực (NRT). Điều này có nghĩa là tài liệu mới được lập chỉ mục sẽ nhanh chóng có sẵn cho các tìm kiếm, thường là trong vòng một giây.

Mô hình hoạt động
Thêm dữ liệu: Khi một tài liệu mới được thêm vào index, Elasticsearch sẽ tự động chia nhỏ tài liệu đó và lưu trữ vào các shard. Các shard sẽ được phân phối trên các node trong cluster.

Tìm kiếm dữ liệu: Khi có một truy vấn tìm kiếm, Elasticsearch sẽ phân tán truy vấn đó đến tất cả các shard liên quan. Mỗi shard sẽ tìm kiếm trong phần dữ liệu của nó và trả về kết quả. Elasticsearch sau đó sẽ hợp nhất các kết quả từ tất cả các shard và trả về kết quả tổng hợp cho người dùng.

Cập nhật và xóa dữ liệu: Khi một tài liệu được cập nhật hoặc xóa, Elasticsearch sẽ tìm và sửa đổi hoặc xóa tài liệu đó trong các shard tương ứng. Các thay đổi này cũng sẽ được sao chép vào các bản sao (replica) của shard để đảm bảo tính nhất quán và độ tin cậy.

Elasticsearch cung cấp các API RESTful cho các thao tác CRUD (Create, Read, Update, Delete). Dưới đây là các cú pháp cơ bản để thực hiện các thao tác này:

 1. Create (Tạo mới tài liệu)

 Tạo tài liệu với ID tự động
```
json
POST /index_name/_doc/
{
  "field1": "value1",
  "field2": "value2"
}
```


 Tạo tài liệu với ID xác định
```
json
PUT /index_name/_doc/1
{
  "field1": "value1",
  "field2": "value2"
}
```

 2. Read (Đọc tài liệu)

 Đọc tài liệu theo ID
```
json
GET /index_name/_doc/1
```

 Tìm kiếm tài liệu với query
```
json
GET /index_name/_search
{
  "query": {
    "match": {
      "field1": "value1"
    }
  }
}
```


 3. Update (Cập nhật tài liệu)

 Cập nhật tài liệu một phần (Partial Update)
```
json
POST /index_name/_update/1
{
  "doc": {
    "field1": "new_value1"
  }
}
```


 Thay thế tài liệu hoàn toàn
```
json
PUT /index_name/_doc/1
{
  "field1": "new_value1",
  "field2": "new_value2"
}
```


 4. Delete (Xóa tài liệu)

 Xóa tài liệu theo ID
```
json
DELETE /index_name/_doc/1
```


 5. Bulk Operations (Thao tác hàng loạt)

 Thực hiện nhiều thao tác trong một yêu cầu duy nhất
```
json
POST /index_name/_bulk
{ "index": { "_id": "1" } }
{ "field1": "value1", "field2": "value2" }
{ "update": { "_id": "1" } }
{ "doc": { "field1": "new_value1" } }
{ "delete": { "_id": "1" } }
```

 6. Tạo chỉ mục (Create Index)

```
json
PUT /index_name
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "field1": { "type": "text" },
      "field2": { "type": "keyword" }
    }
  }
}
```

 7. Xóa chỉ mục (Delete Index)

```
json
DELETE /index_name
```


 8. Kiểm tra sự tồn tại của tài liệu (Check if a Document Exists)

```
json
HEAD /index_name/_doc/1
```

 9. Kiểm tra sự tồn tại của chỉ mục (Check if an Index Exists)

```
json
HEAD /index_name
```

 10. Lấy tất cả tài liệu trong chỉ mục

```
json
GET /index_name/_search
{
  "query": {
    "match_all": {}
  }
}
```

Trong Elasticsearch, cú pháp tìm kiếm (search syntax) được thực hiện thông qua các truy vấn (queries) trong ngôn ngữ truy vấn JSON (JSON query language). Dưới đây là một số cú pháp tìm kiếm cơ bản và phổ biến trong Elasticsearch:


 1. Match Query

`match` query tìm kiếm các tài liệu phù hợp với văn bản đã cho. Đây là truy vấn toàn văn (full-text query).

```
GET /index_name/_search
{
  "query": {
    "match": {
      "field_name": "search text"
    }
  }
}
```


 2. Term Query

`term` query tìm kiếm các tài liệu chứa từ khóa chính xác đã cho. Đây là truy vấn chính xác (exact-match query).

```
GET /index_name/_search
{
  "query": {
    "term": {
      "field_name": "exact term"
    }
  }
}
```


 3. Bool Query

`bool` query kết hợp nhiều truy vấn khác nhau bằng các toán tử logic như `must`, `should`, `must_not`.

```
GET /index_name/_search
{
  "query": {
    "bool": {
      "must": [
        { "match": { "field1": "text1" }},
        { "match": { "field2": "text2" }}
      ],
      "filter": [
        { "term": { "field3": "value3" }}
      ],
      "must_not": [
        { "term": { "field4": "value4" }}
      ]
    }
  }
}
```

 4. Range Query

`range` query tìm kiếm các tài liệu với các giá trị trong một phạm vi nhất định.

```
GET /index_name/_search
{
  "query": {
    "range": {
      "numeric_field": {
        "gte": 10,
        "lte": 20
      }
    }
  }
}
```

 5. Wildcard Query

`wildcard` query tìm kiếm các tài liệu với từ khóa có chứa ký tự đại diện (wildcard characters) như `*` và `?`.

```
GET /index_name/_search
{
  "query": {
    "wildcard": {
      "field_name": "foo*"
    }
  }
}
```

 6. Fuzzy Query

`fuzzy` query tìm kiếm các tài liệu chứa từ khóa gần đúng với từ khóa đã cho (thường là cho phép một số lỗi chính tả).

```
GET /index_name/_search
{
  "query": {
    "fuzzy": {
      "field_name": {
        "value": "fuzziness",
        "fuzziness": "AUTO"
      }
    }
  }
}
```

 7. Aggregation

Aggregation dùng để nhóm và tính toán số liệu trên dữ liệu tìm kiếm.

```
GET /index_name/_search
{
  "size": 0,
  "aggs": {
    "average_value": {
      "avg": {
        "field": "numeric_field"
      }
    }
  }
}
```


 8. Multi-match Query

`multi_match` query tìm kiếm trên nhiều trường khác nhau.

```
GET /index_name/_search
{
  "query": {
    "multi_match": {
      "query": "search text",
      "fields": ["field1", "field2", "field3"]
    }
  }
}
```


 9. Filter Context

Filter context dùng để lọc các tài liệu mà không ảnh hưởng đến điểm số (score) của các tài liệu.

```
GET /index_name/_search
{
  "query": {
    "bool": {
      "filter": [
        { "term": { "status": "active" }}
      ]
    }
  }
}
```
### Aggregations

An aggregation summarizes your data as metrics, statistics, and other analytics. 

#### Analyze the data to show the categories of news headlines in our dataset
Syntax:
```
GET enter_name_of_the_index_here/_search
{
  "aggs": {
    "name your aggregation here": {
      "specify aggregation type here": {
        "field": "name the field you want to aggregate here",
        "size": state how many buckets you want returned here
      }
    }
  }
}
```

### A combination of query and aggregation request

#### Search for the most significant term in a category

Syntax:
```
GET enter_name_of_the_index_here/_search
{
  "query": {
    "match": {
      "Enter the name of the field": "Enter the value you are looking for"
    }
  },
  "aggregations": {
    "Name your aggregation here": {
      "significant_text": {
        "field": "Enter the name of the field you are searching for"
      }
    }
  }
}
```


### Precision and Recall

#### Increasing Recall

Syntax:
```
GET enter_name_of_index_here/_search
{
  "query": {
    "match": {
      "Specify the field you want to search": {
        "query": "Enter search terms"
      }
    }
  }
}
```

Phản hồi mong đợi từ Elaticsearch:

Theo mặc định, truy vấn so khớp sử dụng logic "HOẶC". Nếu một tài liệu chứa một trong các cụm từ tìm kiếm, Elaticsearch sẽ coi tài liệu đó là một hit.

Logic "OR" dẫn đến số lần truy cập cao hơn, do đó tăng khả năng thu hồi. Tuy nhiên, các lần truy cập có liên quan lỏng lẻo đến truy vấn và do đó làm giảm độ chính xác.


#### Tăng độ chính xác
Chúng ta có thể tăng độ chính xác bằng cách thêm toán tử "và" vào truy vấn.
Syntax:
```
GET enter_name_of_index_here/_search
{
  "query": {
    "match": {
      "Specify the field you want to search": {
        "query": "Enter search terms",
        "operator": "and"
      }
    }
  }
}
```

Phản hồi mong đợi từ Elaticsearch: 

 Toán tử "AND" sẽ mang lại kết quả khớp chính xác hơn, do đó tăng độ chính xác. Tuy nhiên, nó sẽ làm giảm số lượt truy cập được trả về, dẫn đến khả năng thu về thấp hơn.. 

#### minimum_should_match
Tham số này cho phép bạn chỉ định số lượng thuật ngữ tối thiểu mà tài liệu phải có trong kết quả tìm kiếm.
Tham số này cho phép bạn kiểm soát nhiều hơn độ chính xác tinh chỉnh và thu hồi tìm kiếm của bạn.


Syntax:
```
GET enter_name_of_index_here/_search
{
  "query": {
    "match": {
      "headline": {
        "query": "Enter search term here",
        "minimum_should_match": Enter a number here
      }
    }
  }
}
```
Phản hồi mong đợi từ Elaticsearch:  
Với tham số minimum_should_match, chúng ta đã có thể tinh chỉnh cả độ chính xác và thu hồi!

Đây chỉ là một số cú pháp cơ bản trong Elasticsearch. Bạn có thể kết hợp các truy vấn này và sử dụng các tùy chọn khác để tùy chỉnh tìm kiếm theo nhu cầu cụ thể của mình.
