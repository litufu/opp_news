'''
每股指标
基本每股收益(元)
扣非每股收益(元)
稀释每股收益(元)
每股净资产(元)
每股公积金(元)
每股未分配利润(元)
每股经营现金流(元)
成长能力指标
营业总收入(元)
毛利润(元)
归属净利润(元)
扣非净利润(元)
营业总收入同比增长(%)
归属净利润同比增长(%)
扣非净利润同比增长(%)
营业总收入滚动环比增长(%)
归属净利润滚动环比增长(%)
扣非净利润滚动环比增长(%)
盈利能力指标
净资产收益率(加权)(%)
净资产收益率(扣非/加权)(%)
总资产收益率(加权)(%)
毛利率(%)
净利率(%)
收益质量指标
预收账款/营业总收入
销售净现金流/营业总收入
经营净现金流/营业总收入
实际税率(%)
财务风险指标
流动比率
速动比率
现金流量比率
资产负债率(%)
权益系数
产权比率
营运能力指标
总资产周转天数(天)
存货周转天数(天)
应收账款周转天数(天)
总资产周转率(次)
存货周转率(次)
应收账款周转率(次)

Per share indicator
Basic earnings per share (yuan)
Deducting non earnings per share (yuan)
Diluted earnings per share (yuan)
Net assets per share (yuan)
Per share provident fund (yuan)
Undistributed profit per share (yuan)
Operating cash flow per share (yuan)
Growth ability indicators
Total operating revenue (yuan)
Gross profit (yuan)
Net profit attributable (yuan)
Deducting non net profit (yuan)
Year on year growth of total operating revenue (%)
Year on year increase in attributable net profit (%)
Non recurring net profit growth year-on-year (%)
Rolling month on month growth of total operating revenue (%)
Rolling month on month increase in attributable net profit (%)
Rolling month on month growth of non recurring net profit (%)
Profitability indicators
Return on equity (weighted) (%)
Return on equity (excluding non GAAP/weighted) (%)
Return on total assets (weighted) (%)
Gross profit margin (%)
Net profit margin (%)
Revenue quality indicators
Accounts receivable/total operating revenue
Net cash flow from sales/total operating revenue
Operating net cash flow/total operating income
Actual tax rate (%)
Financial risk indicators
Current ratio
Quick ratio
Cash flow ratio
Asset liability ratio (%)
Equity coefficient
Property ownership ratio
Operational capability indicators
Total asset turnover days (days)
Inventory turnover days (days)
Accounts receivable turnover days (days)
Total asset turnover rate (times)
Inventory turnover rate (times)
Accounts receivable turnover rate (times)
'''


finance_indicator_names = [
    {"cn":"基本每股收益","en":"beps","display":"基本每股收益(元)"},
    {"cn":"扣非每股收益","en":"dneps","display":"扣非每股收益(元)"},
    {"cn":"摊薄每股收益","en":"deps","display":"摊薄每股收益(元)"},
    {"cn":"稀释每股收益","en":"deps","display":"稀释每股收益(元)"},
    {"cn":"每股净资产","en":"neps","display":"每股净资产(元)"},
    {"cn":"每股公积金","en":"ppfs","display":"每股公积金(元)"},
    {"cn":"每股未分配利润","en":"udlps","display":"每股未分配利润(元)"},
    {"cn":"每股经营现金流","en":"ocfps","display":"每股经营现金流(元)"},
    {"cn":"营业总收入","en":"total_operating_revenue","display":"营业总收入(元)"},
    {"cn":"毛利润","en":"gross_profit","display":"毛利润(元)"},
    {"cn":"归属净利润","en":"net_profit_attributable","display":"归属净利润(元)"},
    {"cn":"扣非净利润","en":"deducting_non_net_profit","display":"扣非净利润(元)"},
    {"cn":"营业总收入同比增长","en":"yoy_total_operating_revenue","display":"营业总收入同比增长(%)"},
    {"cn":"归属净利润同比增长","en":"yoy_net_profit_attributable","display":"归属净利润同比增长(%)"},
    {"cn":"扣非净利润同比增长","en":"yoy_deducting_non_net_profit","display":"扣非净利润同比增长(%)"},
    {"cn":"营业总收入滚动环比增长","en":"mom_total_operating_revenue","display":"营业总收入滚动环比增长(%)"},
    {"cn":"归属净利润滚动环比增长","en":"mom_net_profit_attributable","display":"归属净利润滚动环比增长(%)"},
    {"cn":"扣非净利润滚动环比增长","en":"mom_deducting_non_net_profit","display":"扣非净利润滚动环比增长(%)"},
    {"cn":"净资产收益率(加权)","en":"roe_weighted","display":"净资产收益率(加权)(%)"},
    {"cn":"摊薄净资产收益率","en":"roe_weighted","display":"摊薄净资产收益率(%)"},
    {"cn":"净资产收益率(扣非/加权)","en":"roe_excluding_non_gaap_weighted","display":"净资产收益率(扣非/加权)(%)"},
    {"cn":"总资产收益率(加权)","en":"roa_weighted","display":"总资产收益率(加权)(%)"},
    {"cn":"摊薄总资产收益率","en":"roa_weighted","display":"摊薄总资产收益率(%)"},
    {"cn":"毛利率","en":"gross_profit_margin","display":"毛利率(%)"},
    {"cn":"净利率","en":"net_profit_margin","display":"净利率(%)"},
    {"cn":"预收账款/营业总收入","en":"accounts_receivable_to_tor","display":"预收账款/营业总收入"},
    {"cn":"销售净现金流/营业总收入","en":"net_cash_flow_from_sales_to_tor","display":"销售净现金流/营业总收入"},
    {"cn":"经营净现金流/营业总收入","en":"operating_net_cash_flow_to_tor","display":"经营净现金流/营业总收入"},
    {"cn":"实际税率","en":"actual_tax_rate","display":"实际税率(%)"},
    {"cn":"流动比率","en":"current_ratio","display":"流动比率"},
    {"cn":"速动比率","en":"quick_ratio","display":"速动比率"},
    {"cn":"现金流量比率","en":"cash_flow_ratio","display":"现金流量比率"},
    {"cn":"资产负债率","en":"asset_liability_ratio","display":"资产负债率(%)"},
    {"cn":"权益系数","en":"equity_coefficient","display":"权益系数"},
    {"cn":"产权比率","en":"property_ownership_ratio","display":"产权比率"},
    {"cn":"总资产周转天数","en":"total_asset_turnover_days","display":"总资产周转天数(天)"},
    {"cn":"存货周转天数","en":"inventory_turnover_days","display":"存货周转天数(天)"},
    {"cn":"应收账款周转天数","en":"accounts_receivable_turnover_days","display":"应收账款周转天数(天)"},
    {"cn":"总资产周转率","en":"total_asset_turnover_rate","display":"总资产周转率(次)"},
    {"cn":"存货周转率","en":"inventory_turnover_rate","display":"存货周转率(次)"},
    {"cn":"应收账款周转率","en":"accounts_receivable_turnover_rate","display":"应收账款周转率(次)"}
]