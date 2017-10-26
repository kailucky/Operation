常见的DNS解析类型包括A、MX、NS、CNAME等。利用dnspython的dns.resolver.query方法可以简单实现这些DNS类型的查询，为后面要实现的功能提供数据来源。比如，对一个使用DNS轮循业务的域名进行可用性监控。

simple1 -- A记录

simple2 -- MX记录

simple3 -- NS记录

simple4 -- CNAME记录

simple5 -- DNS域名轮循业务监控