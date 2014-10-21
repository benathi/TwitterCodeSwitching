# encoding: UTF-8
require 'thailang4r/word_breaker'
word_breaker = ThaiLang::WordBreaker.new
puts word_breaker.break_into_words("ฉันกินข้าว")
#puts word_breaker.break_into_words("ขอบคุณนะคะที่มากันวันนี้")
#puts "แต่ประโยคที่โยพูดออกมาวันนั้นมันสืบเนื่องมาจากครั้งแรกที่คุณบีออกมาให้สัมภาษณ์ว่าเรามีปัญหากันเรื่องธุรกิจ จนโยถูกผลกระทบจากสังคมรอบด้านที่ตัดสินว่าโยโกงเขา"