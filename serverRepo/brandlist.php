<?php
include "header.php"  ;
include "slider.php" ;
include "class/brand_class.php"
?>
<?php
$brand = new brand ;
$show_brand = $brand ->show_brand() ;
?>
<div class="admin-content-right">   
<div class="admin-content-right-category_list">
            <h1> Danh sách loại sản phẩm </h1>
            <table>
                <tr> 
                    <th> stt</th>
                    <th> id </th>
                    <th> Danh mục </th>
                    <th> Sản phẩm</th>
                    <th> Tùy biến</th>
                </tr>
                <?php
                if($show_brand){$i = 0 ;
                   while($result = $show_brand->fetch_assoc() ){
                        $i++ ; 
                ?>
                <tr> 
                    <th>  <?php echo $i ?></th>
                    <th> <?php echo $result['brand_id'] ?></th>
                    <th> <?php echo $result['category_name'] ?></th>
                    <th> <?php echo $result['brand_name'] ?></th>
                    <th> <a href="brandedit.php?brand_id=<?php echo $result['brand_id'] ?>"> sửa </a> | <a href="branddelete.php?brand_id=<?php echo $result['brand_id'] ?>"> xóa </a></th>
                </tr>
                <?php
                }
            }
             ?>   
            </table>
</div>
</div>
</html>